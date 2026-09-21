from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BusBooking(models.Model):
    _name = 'bus.booking'
    _description = 'Bus Booking'

    name = fields.Char(
        string='Booking Reference',
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('bus.booking'),
        copy=False,
    )
    customer_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
    )
    trip_id = fields.Many2one(
        'bus.trip',
        string='Trip',
        required=True,
    )
    booking_seat_ids = fields.Many2many(
        'bus.trip.seat',
        string='Seats',
        required=True,
        help='Only available seats for the selected trip can be chosen.',
    )
    seat_count = fields.Integer(
        string='Seat Count',
        compute='_compute_seat_count',
        store=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='trip_id.currency_id',
        readonly=True,
    )
    fare_per_seat = fields.Monetary(
        string='Fare per Seat',
        related='trip_id.fare',
        readonly=True,
        currency_field='currency_id',
    )
    total_fare = fields.Monetary(
        string='Total Fare',
        compute='_compute_total_fare',
        store=True,
        currency_field='currency_id',
        help='Automatically calculated from fare per seat multiplied by seat count.',
    )
    payment_status = fields.Selection(
        [('unpaid', 'Unpaid'),
         ('paid', 'Paid'),
         ('refunded', 'Refunded')],
        string='Payment Status',
        default='unpaid',
        required=True,
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('cancelled', 'Cancelled')],
        string='Status',
        default='draft',
        required=True,
        help='Workflow: Draft bookings can be confirmed to reserve seats and create an invoice; confirmed bookings can be cancelled to release the seats.',
    )
    invoice_id = fields.Many2one(
        'account.move',
        string='Invoice',
        readonly=True,
        copy=False,
    )
    booking_date = fields.Datetime(
        string='Booking Date',
        default=fields.Datetime.now,
    )
    trip_date = fields.Datetime(
        string='Trip Date',
        related='trip_id.departure_datetime',
        store=True,
    )
    route_name = fields.Char(
        string='Route',
        related='trip_id.route_id.name',
        store=True,
    )

    @api.depends('booking_seat_ids')
    def _compute_seat_count(self):
        for booking in self:
            booking.seat_count = len(booking.booking_seat_ids)

    @api.depends('fare_per_seat', 'seat_count')
    def _compute_total_fare(self):
        for booking in self:
            booking.total_fare = booking.fare_per_seat * booking.seat_count

    @api.onchange('trip_id')
    def _onchange_trip_id(self):
        if self.trip_id:
            self.booking_seat_ids = [(5, 0, 0)]

    @api.constrains('booking_seat_ids', 'trip_id')
    def _check_seat_availability(self):
        for booking in self:
            if not booking.booking_seat_ids or not booking.trip_id:
                continue
            invalid = booking.booking_seat_ids.filtered(
                lambda s: s.trip_id != booking.trip_id
            )
            if invalid:
                raise ValidationError(
                    'One or more selected seats do not belong to this trip.'
                )
            overlapping = self.env['bus.booking'].search([
                ('trip_id', '=', booking.trip_id.id),
                ('state', 'in', ['draft', 'confirmed']),
                ('id', '!=', booking.id),
                ('booking_seat_ids', 'in', booking.booking_seat_ids.ids),
            ])
            if overlapping:
                raise ValidationError(
                    'One or more selected seats are already booked on this trip.'
                )

    def action_confirm(self):
        for booking in self:
            if booking.state != 'draft':
                raise ValidationError('Only draft bookings can be confirmed.')
            if booking.trip_id.state != 'scheduled':
                raise ValidationError(
                    'The trip must be confirmed before bookings can be confirmed.'
                )
            unavailable = booking.booking_seat_ids.filtered(
                lambda s: s.state != 'available'
            )
            if unavailable:
                raise ValidationError(
                    'Selected seats are not available.'
                )
            booking.booking_seat_ids.write({'state': 'booked'})
            booking.state = 'confirmed'
            booking._create_invoice()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Booking Confirmed!',
                'type': 'rainbow_man',
            }
        }

    def action_cancel(self):
        for booking in self:
            if booking.state not in ('draft', 'confirmed'):
                raise ValidationError(
                    'Only draft or confirmed bookings can be cancelled.'
                )
            if booking.state == 'confirmed':
                booking.booking_seat_ids.write({'state': 'available'})
            booking.state = 'cancelled'
            if booking.invoice_id and booking.invoice_id.state != 'cancelled':
                booking.invoice_id.button_cancel()

    def _create_invoice(self):
        self.ensure_one()
        invoice_lines = []
        for seat in self.booking_seat_ids:
            invoice_lines.append((0, 0, {
                'name': f"Bus Ticket - {self.trip_id.name} - Seat {seat.seat_number}",
                'quantity': 1,
                'price_unit': self.fare_per_seat,
            }))
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.customer_id.id,
            'invoice_line_ids': invoice_lines,
        })
        invoice.action_post()
        self.invoice_id = invoice
        return invoice

    def action_view_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'view_mode': 'form',
        }

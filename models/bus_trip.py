from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BusTrip(models.Model):
    _name = 'bus.trip'
    _description = 'Bus Trip'

    name = fields.Char(
        string='Trip Name',
        compute='_compute_name',
        store=True,
    )
    route_id = fields.Many2one(
        'bus.route',
        string='Route',
        required=True,
    )
    vehicle_id = fields.Many2one(
        'bus.vehicle',
        string='Vehicle',
        required=True,
    )
    driver_id = fields.Many2one(
        'bus.driver',
        string='Driver',
        required=True,
    )
    departure_datetime = fields.Datetime(
        string='Departure',
        required=True,
    )
    arrival_datetime = fields.Datetime(
        string='Arrival',
    )
    fare = fields.Monetary(
        string='Fare',
        currency_field='currency_id',
        required=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id,
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('scheduled', 'Scheduled'),
         ('departed', 'Departed'),
         ('completed', 'Completed'),
         ('cancelled', 'Cancelled')],
        string='Status',
        default='draft',
        required=True,
    )
    trip_seat_ids = fields.One2many(
        'bus.trip.seat',
        'trip_id',
        string='Trip Seats',
    )
    total_seats = fields.Integer(
        string='Total Seats',
        related='vehicle_id.total_seats',
        readonly=True,
    )
    available_seats_count = fields.Integer(
        string='Available Seats',
        compute='_compute_available_seats_count',
    )
    booked_seats_count = fields.Integer(
        string='Booked Seats',
        compute='_compute_booked_seats_count',
        store=True,
    )
    occupancy_rate = fields.Float(
        string='Occupancy Rate',
        compute='_compute_occupancy_rate',
        store=True,
        aggregator='avg',
    )

    @api.depends('route_id', 'departure_datetime')
    def _compute_name(self):
        for trip in self:
            if trip.route_id and trip.departure_datetime:
                trip.name = f"{trip.route_id.name} / {trip.departure_datetime:%Y-%m-%d %H:%M}"
            else:
                trip.name = ''

    @api.depends('trip_seat_ids', 'trip_seat_ids.state')
    def _compute_available_seats_count(self):
        for trip in self:
            trip.available_seats_count = len(
                trip.trip_seat_ids.filtered(lambda s: s.state == 'available')
            )

    @api.depends('trip_seat_ids', 'trip_seat_ids.state')
    def _compute_booked_seats_count(self):
        for trip in self:
            trip.booked_seats_count = len(
                trip.trip_seat_ids.filtered(lambda s: s.state == 'booked')
            )

    @api.depends('booked_seats_count', 'total_seats')
    def _compute_occupancy_rate(self):
        for trip in self:
            if trip.total_seats > 0:
                trip.occupancy_rate = trip.booked_seats_count / trip.total_seats * 100
            else:
                trip.occupancy_rate = 0.0

    @api.onchange('route_id')
    def _onchange_route_id(self):
        if self.route_id:
            self.fare = self.route_id.base_fare
            self.currency_id = self.route_id.currency_id

    def action_confirm(self):
        for trip in self:
            if trip.state != 'draft':
                raise ValidationError('Only draft trips can be confirmed.')
            if trip.departure_datetime and trip.departure_datetime < fields.Datetime.now():
                raise ValidationError('Cannot confirm a trip with a past departure time.')
            if not trip.trip_seat_ids:
                seat_vals_list = []
                for seat in trip.vehicle_id.seat_ids:
                    seat_vals_list.append({
                        'trip_id': trip.id,
                        'seat_id': seat.id,
                        'state': 'available',
                    })
                self.env['bus.trip.seat'].create(seat_vals_list)
            trip.state = 'scheduled'

    def action_start_trip(self):
        for trip in self:
            if trip.state != 'scheduled':
                raise ValidationError('Only scheduled trips can be started.')
            trip.state = 'departed'

    def action_complete(self):
        for trip in self:
            if trip.state != 'departed':
                raise ValidationError('Only departed trips can be completed.')
            trip.state = 'completed'

    def action_cancel(self):
        for trip in self:
            if trip.state == 'completed':
                raise ValidationError('Cannot cancel a completed trip.')
            trip.state = 'cancelled'

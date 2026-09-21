from odoo import models, fields, api


class BusVehicle(models.Model):
    _name = 'bus.vehicle'
    _description = 'Bus Vehicle'

    name = fields.Char(string='Bus Name', required=True)
    registration_no = fields.Char(string='Registration No.', required=True)
    vehicle_type = fields.Selection([
        ('ac', 'AC'),
        ('non_ac', 'Non-AC'),
    ], string='Vehicle Type', required=True)
    total_seats = fields.Integer(
        string='Total Seats',
        required=True,
        help='Total seats on this vehicle. Drives the automatic seat generation.',
    )
    active = fields.Boolean(string='Active', default=True)

    seat_ids = fields.One2many(
        'bus.seat',
        'vehicle_id',
        string='Seats',
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id,
    )

    _unique_registration_no = models.Constraint(
        'UNIQUE(registration_no)',
        'Error: A bus with this registration number already exists!',
    )

    def action_generate_seats(self):
        self.ensure_one()
        if self.seat_ids:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Seats Already Generated',
                    'message': 'Seats have already been generated for this vehicle.',
                    'type': 'warning',
                }
            }
        seat_vals_list = []
        for i in range(1, self.total_seats + 1):
            seat_type = 'window' if i % 2 == 1 else 'aisle'
            seat_vals_list.append({
                'seat_number': str(i),
                'seat_type': seat_type,
                'vehicle_id': self.id,
            })
        self.env['bus.seat'].create(seat_vals_list)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Seats Generated',
                'message': f'{self.total_seats} seats have been generated successfully.',
                'type': 'success',
            }
        }
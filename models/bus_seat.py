from odoo import models, fields, api


class BusSeat(models.Model):
    _name = 'bus.seat'
    _description = 'Bus Seat'

    seat_number = fields.Char(string='Seat Number', required=True)
    seat_type = fields.Selection([
        ('window', 'Window'),
        ('aisle', 'Aisle'),
    ], string='Seat Type', required=True)
    vehicle_id = fields.Many2one(
        'bus.vehicle',
        string='Vehicle',
        required=True,
        ondelete='cascade',
    )

    _unique_vehicle_seat = models.Constraint(
        'UNIQUE(vehicle_id, seat_number)',
        'Error: Seat number already exists for this vehicle!',
    )
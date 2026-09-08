from odoo import models, fields


class BusTripSeat(models.Model):
    _name = 'bus.trip.seat'
    _description = 'Bus Trip Seat'

    trip_id = fields.Many2one(
        'bus.trip',
        string='Trip',
        required=True,
        ondelete='cascade',
    )
    seat_id = fields.Many2one(
        'bus.seat',
        string='Seat',
        required=True,
    )
    seat_number = fields.Char(
        string='Seat Number',
        related='seat_id.seat_number',
        store=True,
        readonly=True,
    )
    state = fields.Selection(
        [('available', 'Available'),
         ('booked', 'Booked'),
         ('blocked', 'Blocked')],
        string='Status',
        default='available',
        required=True,
    )

    _unique_trip_seat = models.Constraint(
        'UNIQUE(trip_id, seat_id)',
        'Error: This seat already exists for this trip!',
    )

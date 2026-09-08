from odoo import models, fields, api


class BusRoute(models.Model):
    _name = 'bus.route'
    _description = 'Bus Route'

    name = fields.Char(string='Route Name', required=True)
    origin = fields.Char(string='Origin', required=True)
    destination = fields.Char(string='Destination', required=True)
    distance_km = fields.Float(string='Distance (km)')
    base_fare = fields.Monetary(string='Base Fare', currency_field='currency_id', required=True)
    active = fields.Boolean(string='Active', default=True)

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id,
    )

    _unique_origin_destination = models.Constraint(
        'UNIQUE(origin, destination)',
        'Error: A route with the same origin and destination already exists!',
    )

    @api.constrains('origin', 'destination')
    def _check_origin_different_destination(self):
        for record in self:
            if record.origin and record.destination and record.origin.lower() == record.destination.lower():
                raise models.ValidationError(
                    'Error: Origin and destination cannot be the same!'
                )
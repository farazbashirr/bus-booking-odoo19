from odoo import models, fields, api


class BusDriver(models.Model):
    _name = 'bus.driver'
    _description = 'Bus Driver'

    name = fields.Char(string='Driver Name', required=True)
    phone = fields.Char(string='Phone')
    license_no = fields.Char(string='License No.', required=True)
    active = fields.Boolean(string='Active', default=True)

    _unique_license_no = models.Constraint(
        'UNIQUE(license_no)',
        'Error: A driver with this license number already exists!',
    )
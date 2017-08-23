# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

DATE_UNIT = [('day', _("Day")),
        ('month', _("Month")),
        ('year', _("Year")),]

class ClSubscription(models.Model):
    _name = 'cl.subscription'
    _description = "Cl Subscription"
    _order = 'name'

    name = fields.Char(size=128)
    description = fields.Text()
    product_id = fields.Many2one('product.product')
    partner_id = fields.Many2one('res_partner')
    date_begin = fields.Date()
    delay = fields.Integer()
    delay_unit = fields.Selection(DATE_UNIT)
    date_end = fields.Date()
    price = fields.Float()
    tacit_agreement = fields.Boolean()
    cancellation = fields.Integer()
    cancellation_unit = fields.Selection(DATE_UNIT)
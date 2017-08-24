# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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
    partner_id = fields.Many2one('res.partner')
    date_begin = fields.Date(_("Date begin"))
    delay = fields.Integer()
    delay_unit = fields.Selection(DATE_UNIT, _("Delay unit"))
    date_end = fields.Date(_("Date fin"), compute='compute_date_end', store=True)
    quantity = fields.Float(_("Quantity"))
    price = fields.Float()
    tacit_agreement = fields.Boolean(_("Tarif agreement"))
    cancellation = fields.Integer()
    cancellation_unit = fields.Selection(DATE_UNIT, _("Cancellation unit"))
    
    @api.onchange('delay','delay_unit','date_begin')
    def compute_date_end(self):
        date_end = fields.Date.from_string(self.date_begin)
        if self.delay_unit == 'days':
            date_end += timedelta(days=self.delay)
        elif self.delay_unit == 'month':
            date_end += relativedelta(months=self.delay)
            date_end -= timedelta(days=1)
        elif self.delay_unit == 'year':
            date_end += relativedelta(years=self.delay) 
            date_end -= timedelta(days=1)
        self.date_end = fields.Date.to_string(date_end)
        
    @api.model
    def create(self, vals):
        new_subscription = super(ClSubscription, self).create(vals)
        
        product_model = self.env['product.product']
        product_obj = product_model.browse([vals['product_id']])
        partner_model = self.env['res.partner']
        partner_obj = partner_model.browse([vals['partner_id']])
        update_values = {}
        update_values['name'] = "%s for %s" % (product_obj.name, partner_obj.name)
        
        date_end = fields.Date.from_string(vals['date_begin'])
        if vals['delay_unit'] == 'days':
            date_end += timedelta(days=vals['delay'])
        elif vals['delay_unit'] == 'month':
            date_end += relativedelta(months=vals['delay'])
            date_end -= timedelta(days=1)
        elif vals['delay_unit'] == 'year':
            date_end += relativedelta(years=vals['delay']) 
            date_end -= timedelta(days=1)
        update_values['date_end'] = fields.Date.to_string(date_end)
        
        new_subscription.with_context(no_update=True).write(update_values)
        
        return new_subscription
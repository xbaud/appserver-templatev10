# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from subscription import DATE_UNIT

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    @api.multi
    def invoice_validate(self):
        res = super(AccountInvoice, self).invoice_validate()
        for invoice in self:
            for invoiceline in invoice.invoice_line_ids:
                product_model = self.env['product.product']
                product_obj = product_model.search([('id', '=', invoiceline.product_id.id)])
                if product_obj:
                    pt_model = self.env['product.template']
                    pt_obj = pt_model.search([('id', '=', product_obj.product_tmpl_id.id)])
                    if pt_obj and pt_obj.type == 'subsc':
                        subscription_model = self.env['cl.subscription']
                        date_end = fields.Date.from_string(invoice.date_invoice)
                        if pt_obj.cl_delay_unit == 'days':
                            date_end += timedelta(days=pt_obj.cl_delay)
                        elif pt_obj.cl_delay_unit == 'month':
                            date_end += relativedelta(months=pt_obj.cl_delay)
                        elif pt_obj.cl_delay_unit == 'year':
                            date_end += relativedelta(years=pt_obj.cl_delay) 
                            date_end -= timedelta(days=1)
                        subscription_dict = {
                            'name' : "%s/%s" % (pt_obj.name, invoice.partner_id.name),
                            'description' : "",
                            'product_id' : invoiceline.product_id.id,
                            'partner_id' : invoice.partner_id.id,
                            'date_begin' : invoice.date_invoice,
                            'delay' : pt_obj.cl_delay,
                            'delay_unit' : pt_obj.cl_delay_unit,
                            'date_end' : date_end.strftime("%Y-%m-%d"),
                            'price' : invoiceline.price_unit,
                            'tacit_agreement' : pt_obj.cl_tacit_agreement,
                            'cancellation' : pt_obj.cl_cancellation,
                            'cancellation_unit' : pt_obj.cl_cancellation_unit,
                        }
                        subscription_model.create(subscription_dict) 
        return res
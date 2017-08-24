# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for orderline in order.order_line:
                pt_model = self.env['product.template']
                pt_obj = pt_model.browse(orderline.product_id.product_tmpl_id.ids)
                if pt_obj and pt_obj.type == 'subsc':
                    subscription_model = self.env['cl.subscription']
                    subscription_dict = {
#                            'name' : "%s/%s" % (pt_obj.name, order.partner_id.name),
                        'description' : "",
                        'product_id' : orderline.product_id.id,
                        'partner_id' : order.partner_id.id,
                        'date_begin' : order.date_order,
                        'delay' : pt_obj.cl_delay,
                        'delay_unit' : pt_obj.cl_delay_unit,
#                           'date_end' : fields.Date.to_string(date_end),
                        'quantity' : orderline.product_uom_qty,
                        'price' : orderline.price_unit,
                        'tacit_agreement' : pt_obj.cl_tacit_agreement,
                        'cancellation' : pt_obj.cl_cancellation,
                        'cancellation_unit' : pt_obj.cl_cancellation_unit,
                    }
                    subscription_model.create(subscription_dict) 
        return res
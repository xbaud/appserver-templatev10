# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    type = fields.Selection([('consu', _('Consumable')),
                             ('service', _('Service')), 
                             ('subsc', _("Subscription"))])
    cl_delay = fields.Integer(_("Delay"))
    cl_delay_unit = fields.Selection([('day', _("Day")),
                                   ('month', _("Month")),
                                   ('year', _("Year"))],
                                   _("Delay unit"))
    cl_tacit_agreement = fields.Boolean(_("Tacit agreement"))
    cl_cancellation = fields.Integer(_("Cancellation"))
    cl_cancellation_unit = fields.Selection([('day', _("Day")),
                                          ('month', _("Month")),
                                          ('year', _("Year"))],
                                          _("Cancellation unit"))

    #def __init__(self, cr, uid, context=None):
    #   super(ProductTemplate, self).__init__(cr, uid)
    #   newOption = ('subsc', _("Subscription"))
    #   typeSelection = self._columns['type'].selection
    #   if newOption not in typeSelection:
    #   typeSelection.append(newOption)

# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
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

    def init(self):
       super(ProductTemplate, self).init()
       newOption = ('subsc', _("Subscription"))
       if 'type' in self._fields:
            typeSelection = self._fields['type'].selection
            if newOption not in typeSelection:
               typeSelection.append(newOption)

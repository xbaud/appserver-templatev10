# -*- coding: utf-8 -*-
# noinspection PyStatementEffect
{
    'name': "Christine",

    'summary': "Christine as an extension of Odoo sales to managed subscription.",

    'description': """Helps you manage your subscription.""",

    'author': "Xavier BAUD",
    'website': "https://www.linkedin.com/in/xavier-baud",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale',
    ],

    # always loaded
    'data': [
        'views/product_template.xml',
    ],
    
    # only loaded in demonstration mode
    'demo': [
    ],
    'application': True,
    'auto_install': False,
    'installable': True
}

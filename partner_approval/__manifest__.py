# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Partner Validation',
    'author': 'Hariprasath.B',
    'depends': [
        'base',
        'sale',
        'account'
    ],
    'version': '13.0.1.1',
    'description': """
        Partner Validation
    """,
    'summary': 'Partner Validation',
    'category': 'Tools',
    'website': 'https://github.com/hari4274/erp-addons/tree/13.0/partner_approval',
    'sequence': 5,
    'data': [
        'views/partner_view.xml',
        'views/sale_view.xml',
    ],
    'qweb': [
    ],
    'images': ['images/screen.png'],
    'application': True,
    'installable': True,
}

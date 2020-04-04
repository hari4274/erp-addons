# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Export Attachments',
    'author': 'Hariprasath.B',
    'depends': [
        'web',
        'base'
    ],
    'version': '13.0.1.1',
    'description': """
        Export Attachments
        In Odoo, We can export all fields but binary fields is very hard to download for many records at once. So planned to give a solution fot that.
    """,
    'summary': 'Export Attachments',
    'category': 'Tools',
    'website': 'https://github.com/hari4274/erp-addons/tree/13.0/export_attachments',
    'sequence': 5,
    'data': [
        'security/ir.model.access.csv',
        'views/export_attachments_view.xml',
    ],
    'qweb': [
    ],
    'images': ['images/screen.png'],
    'application': True,
    'installable': True,
}

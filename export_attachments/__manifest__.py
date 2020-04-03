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
    """,
    'summary': 'Export Attachments',
    'category': 'Tools',
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

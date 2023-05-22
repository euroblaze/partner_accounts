{
    'name': 'Partner-Specific Account Module for Odoo',
    'version': '1.0',
    'category': 'Contacts',
    'summary': 'Partner-Specific Account',
    'author': 'Simplify-ERP™',
    'website': 'https://simplify-erp.de',
    'depends': ['base', 'account', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

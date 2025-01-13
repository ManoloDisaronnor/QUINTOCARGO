# -*- coding: utf-8 -*-
{
    'name': "QuintoCargo",

    'summary': """
        QuintoCargo es una empresa dedicada a mudanzas y almacenaje.""",

    'description': """
        QuintoCargo es una empresa dedicada a mudanzas y almacenaje.
    """,

    'author': "QuintoCargo contributors",
    'website': "https://github.com/ManoloDisaronnor/QUINTOCARGO",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv', 
        'views/menu_view.xml',
        'views/mudanzas_view.xml',
        'views/almacen_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

}

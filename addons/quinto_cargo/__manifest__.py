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
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    'application': True,

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/mudanzas_view.xml',
        'views/mudanzas_reports.xml',
        'views/almacen_view.xml',
        'views/report_layout.xml',
        'views/cliente_reports.xml',
        'views/cliente_view.xml',
        'views/empleado_view.xml',
        'views/bien_asegurado_reports.xml',
        'views/bienes_asegurados_view.xml',
        'views/transporte_view.xml',
        'views/menu_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

}

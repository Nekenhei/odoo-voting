# -*- coding: utf-8 -*-
{
    'name': "voting",

    'summary': """
        Module made to handle the voting process in UNIACME university.""",

    'description': """
        This module allows UNIACME university to perform, track and manage their internal voting processes along
        with a web base interface to subimit those votes.
    """,

    'author': "Esteban Giraldo",
    'website': "https://www.linkedin.com/in/estebangiraldo11/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'CRM',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contact'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

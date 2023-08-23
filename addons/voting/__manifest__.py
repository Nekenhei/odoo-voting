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
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts'],

    # always loaded
    'data': [
        'data/sequence.xml',
        'data/university.xml',
        'data/student.xml',
        
        'security/ir.model.access.csv',
        
        'views/university_views.xml',
        'views/partner_views.xml',
        'views/student_views.xml',
        'views/voting_views.xml',
        'views/menu_views.xml',
    ],
    'application': True,
    'installable': True
}

# -*- coding: utf-8 -*-
{
    'name': "Votación",

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
    'depends': ['contacts', 'website'],

    # always loaded
    'data': [
        'data/sequence.xml',
        'data/university.xml',
        'data/student.xml',
        'data/voting.xml',
        
        'security/ir.model.access.csv',
        
        'views/university_views.xml',
        'views/partner_views.xml',
        'views/student_views.xml',
        'views/voting_views.xml',
        'views/voting_website.xml',
        'views/menu_views.xml',
        
        'wizard/vote_importer_views.xml'
    ],
    'application': True,
    'installable': True
}

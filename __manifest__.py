# -*- coding: utf-8 -*-
{
    'name': "veterinary_clinic_2021",
    'sequence': '2',

    'summary': """
        Ce module est destiné a aidé le personnel de la clinique vétérinaire Zaynabou
        """,

    'description': """
        Dans ce module nous aurons :
        - Enregistrer les animaux selon leur espèce
        - Leur propriétaire comme des clients
        - Les anomalies
        - Et autres ...
    """,

    'author': "Obertys",
    'website': "http://www.obertys.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'account', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/animals_views.xml',
        'Vreport/anitemp.xml',
        'Vreport/vreport.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}

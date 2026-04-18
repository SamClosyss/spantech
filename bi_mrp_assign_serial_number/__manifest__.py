# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    "name" : "Generate Mass serial number fro MRP | Create Mass Serial number from Manufacturing",
    # "version" : "16.0.0.0",
    "category" : "Manufacturing",
    'summary': 'Manufacturing Orders Mass Serial Number Duplicate Serial Number Generator in MRP Orders Mass Produce Serial Number in Manufacturing Import Serial Number in MO Mass Lot Number in Manufacturing Lot Number in MRP Order Mass Sequence Number in Manufacturing',
    "description": """
    
        Manufacturing Mass Serial Number Odoo App helps users to assigning product mass serial number for production order. User have options to generate serial number manually and import serial number from XLS file. Also duplicate serial number generation should be prevented.
    
    """,
    'author': 'BrowseInfo',
    "price": 49,
    "currency": 'EUR',
    'website': 'https://www.browseinfo.com',
    "depends" : ['base','mrp'],
    "data": [
          'security/ir.model.access.csv',
          'data/attachment_sample.xml',
          'wizard/assign_serial_mrp.xml',
          'views/mrp_production_inherit.xml',
    ],
    'license':'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/mqBD2XJsEZ0',
    "images":['static/description/Manufacturing-Mass-Serial-Number-Banner.gif'],
}


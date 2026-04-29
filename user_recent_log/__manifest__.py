# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.

# Author: Aktiv Software.
# mail: odoo@aktivsoftware.com
# Copyright (C) 2015-Present Aktiv Software PVT. LTD.
# Contributions:
# Aktiv Software:
# - Dhara Solanki
# - Mohit Chauhan
# - Harshil Soni
{
    "name": "User Activity Log",
    "summary": """
        The module will show the recent activity of users""",
    "description": """
        The module will show the recent activity of users""",
    "author": "Aktiv Software",
    "website": "http://www.aktivsoftware.com",
    "category": "Extra Tools",
    # "version": "16.0.1.0.0",
    "license": "OPL-1",
    "price": 10.00,
    "currency": "EUR",
    "depends": ["base", "web"],
    "data": [
        "security/ir.model.access.csv",
        "security/user_log_security.xml",
        "data/ir_cron.xml",
        "views/user_activity_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "user_recent_log/static/src/js/*",
        ]
    },
    "images": [
        "static/description/banner.jpg",
    ],
    "installable": True,
    "application": True
}

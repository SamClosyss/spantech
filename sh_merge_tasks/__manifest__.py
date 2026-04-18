# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Merge Project Tasks",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "license": "OPL-1",
    "support": "support@softhealer.com",
    "category": "Project",
    "summary": "Merge Task, Merge Tasks, Merge Projects Tasks, Merge Multiple Project Task, Append Project Task, Combine Project Task, Combine Tasks, Combine Project Tasks, Combine Multiple Tasks, Manage Project Tasks Odoo",
    "description": """Sometimes required to make a single task from the multiple tasks. This module useful to merge multiple project tasks quickly. Your tasks must have the same project for merge tasks. When you merge tasks it merges with all values like description, deadline, timesheet & tags.""",
    # "version": "16.0.1",
    "depends": [

            'project', 'hr_timesheet',
    ],

    "data": [

        "data/sh_merge_tasks_action.xml",
        "views/sh_task.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "images": ["static/description/background.png", ],
    "price": 25,
    "currency": "EUR"
}

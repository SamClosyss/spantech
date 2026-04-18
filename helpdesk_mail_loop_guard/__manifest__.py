{
    "name": "Helpdesk Mail Loop Guard",
    # "version": "16.0.1.0.0",
    "summary": "Prevent infinite mail loops in Helpdesk tickets caused by relay servers",
    "author": "Your Company",
    "license": "LGPL-3",
    "category": "Helpdesk",
    "depends": ["helpdesk", "mail"],
    "data": [
        "data/ir_config_parameter.xml",
    ],
    "installable": True,
    "application": False,
}

from odoo import SUPERUSER_ID, api

from . import controllers, models

PARAMETER = 'trilab_jpk_base.taxoffice_loaded'
from odoo import api


def post_init_handler(env):
    # Elevate privileges while keeping Odoo 19 compatible
    env = env(su=True)

    if not env['ir.config_parameter'].get_param(PARAMETER, False):
        env['jpk.taxoffice'].load_from_xml()
        env['ir.config_parameter'].set_param(PARAMETER, 'true')

    # Hide main menu icon
    menu_data = env['ir.model.data'].search([
        ('name', '=', 'jpk_main_menu'),
        ('module', '=', 'trilab_jpk_base'),
        ('model', '=', 'ir.ui.menu'),
    ], limit=1)

    if menu_data:
        menu_record = env['ir.ui.menu'].browse(menu_data.res_id)
        if menu_record.exists():
            menu_record.write({'active': False})


# noinspection PyUnusedLocal
def uninstall_handler(env):
    env = env(su=True)

    env['ir.config_parameter'].set_param(PARAMETER, None)


# noinspection PyUnusedLocal
# def post_init_handler(env):
#     env = api.Environment(env, SUPERUSER_ID, {})
#     if not env['ir.config_parameter'].get_param(PARAMETER, False):
#         env['jpk.taxoffice'].load_from_xml()
#         env['ir.config_parameter'].set_param(PARAMETER, 'true')
#
#     # hide main menu icon
#     menu_data = env['ir.model.data'].search(
#         [['name', '=', 'jpk_main_menu'], ['module', '=', 'trilab_jpk_base'], ['model', '=', 'ir.ui.menu']]
#     )
#     if menu_data:
#         menu_item = env['ir.ui.menu'].browse([menu_data.res_id])
#         menu_item.write({'active': False})
#
#
# # noinspection PyUnusedLocal
# def uninstall_handler(env):
#     env = api.Environment(env, SUPERUSER_ID, {})
#     # noinspection PyTypeChecker
#     env['ir.config_parameter'].set_param(PARAMETER, None)

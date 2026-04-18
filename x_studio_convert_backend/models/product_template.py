from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # https://spantech.odoo.com/web#id=465&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
    part_code = fields.Char(string="Part Code")
    details = fields.Char(string="Details")
    net_weight = fields.Char(string="Net Weight")
    gross_weight = fields.Char(string="Gross Weight")
    volume_sp = fields.Char(string="Volume")
    pressure = fields.Char(string="Pressure")
    shelf_life = fields.Char(string="Shelf Life")
    product_class = fields.Char(string="Class")
    un_number = fields.Char(string="UN Number")
    shipping_name = fields.Char(string="Shipping Name")
    tunnel_code = fields.Char(string="Tunnel Code")
    sds_number = fields.Char(string="SDS Number")
    label_template = fields.Char(string="Label Template")
    traffic_code = fields.Char(string="Traffic Code")
    size = fields.Char(string="Size")
    valve = fields.Char(string="Valve")
    accuracy = fields.Char(string="Accuracy")
    location = fields.Char(string="Location")

    # https://spantech.odoo.com/web?debug=1#id=734&menu_id=554&cids=7%2C4%2C3%2C2%2C1&action=806&model=project.task&view_type=form
    contract_number = fields.Char(string="Contract Number")

    x_studio_additional_description = fields.Text(string="Additional Description")
    x_studio_contact_name = fields.Char(string="Contact Name")
    x_studio_cylinder_size = fields.Char(string="Cylinder Size")
    x_studio_drawing_reference = fields.Char(string="Drawing Reference")
    x_studio_gas_type = fields.Char(string="Gas Type")
    x_studio_hs_code = fields.Char(string="HS Code")
    x_studio_hs_code_1 = fields.Char(string="Country of Origin")
    x_studio_prices_last_updated = fields.Date(string="Prices Last Updated")
    x_studio_product_notes = fields.Text(string="Product Notes")
    x_studio_reliance_information = fields.Char(string="Reliance Information")
    x_studio_reorder_telephone = fields.Char(string="Reorder Telephone")
    x_studio_secondary_comments = fields.Char(string="Secondary Comments")

    # https://spantech.odoo.com/web#id=909&menu_id=554&cids=7%2C4%2C3%2C2%2C1&action=806&model=project.task&view_type=form
    # Instrument Information
    mml_instrument_number = fields.Integer(string="Instrument Number")
    mml_instrument_owner = fields.Many2one('res.users', string='Instrument Owner', default=lambda self: self.env.user,
                                           tracking=True)
    mml_instrument_name = fields.Char(string="Instrument Name")
    mml_build_name = fields.Char(string="Build Name")
    mml_model = fields.Char(string="Model")
    mml_platform = fields.Char(string="Platform")
    # https://spantech.odoo.com/web#id=913&menu_id=554&cids=7%2C4%2C3%2C2%2C1&action=806&model=project.task&view_type=form
    # mml_responsible_rep = fields.Char(string="Responsible Rep")
    mml_responsible_rep = fields.Many2one('res.partner', string='Responsible Rep', tracking=True)
    mml_commissioning_engineer = fields.Many2one('res.users', string='Commissioning Engineer', tracking=True)
    mml_remote_engineer = fields.Char(string="Remote Engineer")
    mml_warranty = fields.Char(string="Length Of Warranty")
    mml_warranty_expiry = fields.Date(string="Warranty Expiry Date")
    mml_inactive = fields.Boolean(string="Inactive")

    # Commissioning information
    mml_qc_file_date = fields.Date(string="QC File Sign Off Date")
    mml_acceptance_date = fields.Date(string="Acceptance Date")
    mml_commissioning_info_sent = fields.Date(string="Commissioning info sent")
    mml_training_complete = fields.Date(string="Training Complete")
    mml_hs_info_sent = fields.Date(string="H and S info sent")
    mml_outstanding_items = fields.Char(string="Outstanding Items")
    mml_install_date = fields.Date(string="Install Date (Final Day)")
    mml_complete = fields.Boolean(string="Everything Complete, inc outstanding items etc")
    mml_install_report = fields.Date(string="Install report in instrument folder")

    # User Information
    mml_owner = fields.Many2one('res.partner', string="Owner")
    mml_main_user = fields.Many2one('res.partner', string="Main User")
    mml_user_2 = fields.Many2one('res.partner', string="User 2")
    mml_user_3 = fields.Many2one('res.partner', string="User 3")
    mml_notes = fields.Char(string="Notes")

    # Nano Loading Head Information
    mml_nano_head = fields.Boolean(string="Nano Head fitted?")
    mml_scratch = fields.Boolean(string="Scratch & Wear")
    mml_nano_indentation = fields.Boolean(string="Nano Indentation")
    mml_friction = fields.Boolean(string="Friction")
    mml_enhanced_nano = fields.Boolean(string="Enhanced nano Indentation")
    mml_nano_impact = fields.Boolean(string="Nano Impact")
    mml_fretting = fields.Boolean(string="Fretting")
    mml_nano_tribo_test = fields.Boolean(string="NanoTriboTest")

    # Micro Loading Head Info
    mml_micro_head = fields.Boolean(string="Micro Head fitted?")
    mml_micro_scratch = fields.Boolean(string="Micro Scratch & Wear")
    mml_micro_indentation = fields.Boolean(string="Microindentation")
    mml_micro_friction = fields.Boolean(string="Micro Friction")
    mml_enhanced_micro = fields.Boolean(string="Enhanced micro indentation")
    mml_micro_impact = fields.Boolean(string="Micro Impact")

    # Imaging Options
    mml_microscope = fields.Char(string="Microscope")
    mml_nano_positioning_stage = fields.Char(string="Nano Positioning Stage")
    mml_afm = fields.Char(string="AFM")
    mml_rapid_mapping = fields.Boolean(string="Rapid Mapping")
    mml_ht_optics = fields.Boolean(string="HT Optics?")
    mml_nano_wear = fields.Boolean(string="Nano Wear")

    # Environmental Options
    mml_hot_stage = fields.Char(string="Hot Stage")
    mml_cold_stage = fields.Char(string="Cold Stage")
    mml_purge_number = fields.Char(string="Purge/Vacuum Chamber")
    mml_liquid_cell = fields.Char(string="Liquid Cell (NT only)")
    mml_humidity = fields.Boolean(string="Humidity (NT only)")

    # Other Options
    mml_dmct_option = fields.Char(string="DMCT option")
    mml_specials = fields.Char(string="Specials")
    mml_other_options = fields.Char(string="Other Options")
    mml_sales_notes = fields.Char(string="Sales Notes")

    # Upgrades
    mml_detail_upgrades = fields.Char(string="Detail upgrades and dates completed")

    # Technical details
    mml_operating_system = fields.Char(string="Operating System")
    mml_pc_tag_no = fields.Char(string="PC Tag Number")
    mml_serial_no = fields.Char(string="Piseca Serial No.")
    mml_sample_stage_controller = fields.Char(string="Sample Stage Controller")
    mml_av_table_type = fields.Char(string="AV Table Type")
    mml_ssc_serial_number = fields.Char(string="SSC serial number")
    mml_ntx_version = fields.Char(string="NTx Version")
    mml_heat_shield_type = fields.Char(string="Heat Shield Type")
    mml_ntx_serial_no = fields.Char(string="NTx Serial Number")
    mml_impulse = fields.Char(string="Impulse")
    mml_hot_stage_controller = fields.Char(string="Hot Stage Controller")
    mml_indenter_holder = fields.Boolean(string="1.1 mm  Indenter holder")
    mml_hsc_serial_number = fields.Char(string="HSC Serial Number")
    mml_additional_info = fields.Char(string="Additional Info")
    mml_machine_specific_notes = fields.Char(string="Machine Specific Notes")

    # Old Fields
    mml_loading_head = fields.Char(string="Loading Head")
    mml_control_unit = fields.Char(string="Control Unit")
    mml_purge_chamber = fields.Boolean(string="Purge Chamber")

    # Comments
    mml_comments = fields.Char(string="Comments")
    mml_modified_time = fields.Date(string="Modified Time")
    mml_created_time = fields.Date(string="Created Time")
    mml_product_tag_ids = fields.Many2many('product.tag', 'mml_product_tag_product_template_rel', string='Product Tags')

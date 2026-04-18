from odoo import api, fields, models, _


# https://spantech.odoo.com/web?debug=1#id=1002&menu_id=554&cids=7%2C4%2C3%2C2%2C1%2C6%2C8%2C5%2C10%2C9&action=806&model=project.task&view_type=form
class ProductTemplate(models.Model):
    _inherit = 'product.template'


    @api.model
    def _get_default_nrc_1_2_html_text(self):
        # self.nrc1 = 'This is NRC 1'
        return '''
            <div>
                <h6>
                    <strong>WARNING</strong>
                </h6>
                <ul>
                    <li style="margin: 3px 0;">H280 - Contains gas under pressure; may explode if heated.</li>
                    <li style="margin: 3px 0;">P403 - Store in a well-ventilated place.</li>
                </ul> 
            </div> '''

    @api.model
    def _get_default_nrc_3_html_text(self):
        return '''
            <div>
                <h6>
                    <strong>DANGER</strong>
                </h6>
                <ul>
                    <li style="margin: 3px 0;">H270- May cause or intensify fire; oxidiser.</li>
                    <li style="margin: 3px 0;">H280- Contains gas under pressure; may explode if heated.</li>
                    <li style="margin: 3px 0;">P220- Keep away from combustible materials.</li>
                    <li style="margin: 3px 0;">P244- Keep valves and fittings free from oil and grease.</li>
                    <li style="margin: 3px 0;">P370+P376- In case of fire: Stop leak if safe to do so.</li>
                    <li style="margin: 3px 0;">P403- Store in a well ventilated place.</li>
                </ul> 
            </div> '''
    
    @api.model
    def _get_default_nrc_4_5_6_html_text(self):
        return '''
            <div>
                <h6>
                    <strong>DANGER</strong>
                </h6>
                <ul>
                    <li style="margin: 3px 0;">H220 - Extremely flammable gas.</li>
                    <li style="margin: 3px 0;">H280 - Contains gas under pressure; may explode if heated.</li>
                    <li style="margin: 3px 0;">P280 - Wear protective gloves, protective clothing, eye protection.</li>
                    <li style="margin: 3px 0;">P202 - Do not handle until all safety precautions have been read and understood.</li>
                    <li style="margin: 3px 0;">P260 - Do not breathe gas, vapours.</li>
                    <li style="margin: 3px 0;">P210 - Keep away from heat, hot surfaces, sparks, open flames and other ignition sources. No smoking.</li>
                    <li style="margin: 3px 0;">P308+P313 - IF exposed or concerned: Get medical advice.</li>
                    <li style="margin: 3px 0;">P403 - Store in a well-ventilated place.</li>
                </ul> 
            </div> '''
    
    @api.model
    def _get_default_nrc_7_html_text(self):
        return '''
            <div>
                <h6>
                    <strong>DANGER</strong>
                </h6>
                <ul>
                    <li style="margin: 3px 0;">H280 - Contains gas under pressure; may explode if heated.</li>
                    <li style="margin: 3px 0;">H360 - May damage fertility. May damage the unborn child. (inhalation).</li>
                    <li style="margin: 3px 0;">H373 - May cause damage to organs (blood) through prolonged or repeated exposure (inhalation).</li>
                    <li style="margin: 3px 0;">P280 - Wear protective gloves, protective clothing, eye protection.</li>
                    <li style="margin: 3px 0;">P202 - Do not handle until all safety precautions have been read and understood.</li>
                    <li style="margin: 3px 0;">P260 - Do not breathe gas, vapours.</li>
                    <li style="margin: 3px 0;">P308+P313 - IF exposed or concerned: Get medical advice.</li>
                    <li style="margin: 3px 0;">P280 - Wear protective gloves, protective clothing, eye protection.</li>
                    <li style="margin: 3px 0;">P202 - Do not handle until all safety precautions have been read and understood.</li>
                    <li style="margin: 3px 0;">P260 - Do not breathe gas, vapours</li>
                </ul> 
            </div> '''
    
    @api.model
    def _get_default_nrc_8_9_html_text(self):
        return '''
            <div>
                <h6>
                    <strong>DANGER</strong>
                </h6>
                <ul>
                    <li style="margin: 3px 0;">H221 - Flammable gas.</li>
                    <li style="margin: 3px 0;">H280 - Contains gas under pressure; may explode if heated.</li>
                    <li style="margin: 3px 0;">H332 - Harmful if inhaled.</li>
                    <li style="margin: 3px 0;">H360 - May damage the unborn child. Suspected of damaging fertility. (if inhaled)</li>
                    <li style="margin: 3px 0;">H372 - Causes damage to organs through prolonged or repeated exposure (inhalation).</li>
                    <li style="margin: 3px 0;">P280 - Wear protective gloves, protective clothing, eye protection.</li>
                    <li style="margin: 3px 0;">P202 - Do not handle until all safety precautions have been read and understood.</li>
                    <li style="margin: 3px 0;">P260 - Do not breathe gas, vapours.</li>
                    <li style="margin: 3px 0;">P210 - Keep away from heat, hot surfaces, sparks, open flames and other ignition sources. No smoking.</li>
                </ul> 
            </div> '''
    
    @api.model
    def _get_default_nrc_11_html_text(self):
        return '''
            <div>
                <h6>
                    <strong>DANGER</strong>
                </h6>
                <ul>
                    <li style="margin: 3px 0;">H221- Flammable gas.</li>
                    <li style="margin: 3px 0;">H280- Contains gas under pressure; may explode if heated.</li>
                    <li style="margin: 3px 0;">H332- Harmful if inhaled.</li>
                    <li style="margin: 3px 0;">H360- May damage the unborn child. Suspected of damaging fertility(if inhaled).</li>
                    <li style="margin: 3px 0;">H372- Cause damage to organs through prolonged or repeated exposure (inhalation).</li>
                    <li style="margin: 3px 0;">P280- Wear protective gloves, protective clothing eye protection.</li>
                    <li style="margin: 3px 0;">P202- Do not handle untill all safety precautions have been read and understood.</li>
                    <li style="margin: 3px 0;">P260- Do not breathe gas, vapours.</li>
                    <li style="margin: 3px 0;">P210- Keep away from heat, hot surface, sparks, open flames and other ignition sources. No Smoking.</li>
                </ul> 
            </div> '''

    @api.model
    def _get_default_nrc_1_cac_html_text(self):
        return '''
            <div>
                <h6>
                    <strong>WARNING</strong>
                </h6>
                <p>
                    Contains gas under pressure; may explode if heated. Store in a well-ventilated place.
                </p>
            </div>
        '''
    
    @api.model
    def _get_default_nrc_4_cac_html_text(self):
        return '''
            <div>
                <h6>
                    <strong>DANGER</strong>
                </h6>
                <p>
                    Extremely flammable gas. Contains gas under pressure; may explode if heated. Wear protective gloves, protective clothing, eye protection. Do not handle until all safety precautions have been read and understood. Do not breathe gas, vapours. Keep away from heat, hot surfaces, sparks, open flames and other ignition sources. No smoking. IF exposed or concerned: Get medical advice. Store in a well-ventilated place.
                </p>
            </div>
        '''
    
    @api.model
    def _get_default_nrc_1_cac_new_html_text(self):
        return '''
            <div>
                <h6>
                    <strong>WARNING</strong>
                </h6>
                <p>
                    Contains gas under pressure; may explode if heated. Store in a well-ventilated place.
                </p>
            </div>
        '''
    
    @api.model
    def _get_default_nrc_4_cac_new_html_text(self):
        return '''
            <div>
                <h6>
                    <strong>DANGER</strong>
                </h6>
                <p>
                    Extremely flammable gas. Contains gas under pressure; may explode if heated. Wear protective gloves, protective clothing, eye protection. Do not handle until all safety precautions have been read and understood. Do not breathe gas, vapours. Keep away from heat, hot surfaces, sparks, open flames and other ignition sources. No smoking. IF exposed or concerned: Get medical advice. Store in a well-ventilated place.
                </p>
            </div>
        '''
    
    @api.model
    def _get_default_nrc_12_html_text(self):
        return '''
            <div>
                <h6>
                    <strong>DANGER</strong>
                </h6>
                <ul>
                    <li style="margin: 3px 0;">H220 - Extremely flammable gas.</li>
                    <li style="margin: 3px 0;">H280 - Contains gas under pressure; may explode if heated.</li>
                    <li style="margin: 3px 0;">H331 - Toxic if inhaled</li>
                    <li style="margin: 3px 0;">CGA-HG04 - May form explosive mixtures with air</li>
                    <li style="margin: 3px 0;">CGA-HG11 - Symptoms may be delayed</li>
                    <li style="margin: 3px 0;">CGA-HG16 - Extended exposure to gas reduces the ability to smell sulfides.</li>
                    <li style="margin: 3px 0;">CGA-HG01 - May cause frostbite</li>
                    <li style="margin: 3px 0;">P202 - Do not handle until all safety precautions have been read and understood</li>
                    <li style="margin: 3px 0;">P210 - Keep away from Heat, Open flames, Sparks, Hot surfaces. - No smoking</li>
                    <li style="margin: 3px 0;">P260 - Do not breathe gas/vapors</li>
                    <li style="margin: 3px 0;">P271+P403 - Use and store only outdoors or in a well-ventilated place</li>
                    <li style="margin: 3px 0;">P280+P284 - Wear protective gloves, protective clothing, eye protection, respiratory protection</li>
                </ul> 
            </div> '''
    
    @api.model
    def _get_default_nrc_13_html_text(self):
        return '''
            <div>
                <h6>
                    <strong>DANGER</strong>
                </h6>
                <ul>
                    <li style="margin: 3px 0;">H280 - Contains gas under pressure; may explode if heated.</li>
                    <li style="margin: 3px 0;">H314 - Causes severe skin burns and eye damage.</li>
                    <li style="margin: 3px 0;">H332 - Harmful if inhaled</li>
                    <li style="margin: 3px 0;">P260 - Do not breathe gas, vapours.</li>
                    <li style="margin: 3px 0;">P280 - Wear protective gloves, protective clothing, eye protection, face protection.</li>
                    <li style="margin: 3px 0;">P271 - Use only outdoors or in a well-ventilated area.</li>
                    <li style="margin: 3px 0;">P303+P361+P353+P315 - IF ON SKIN : (or hair) Take off immediately all contaminated clothing. Rinse skin with water or shower. Get immediate medical advice.</li>
                    <li style="margin: 3px 0;">P304+P340+P315 - IF INHALED : Remove person to fresh air and keep comfortable for breathing. Get immediate medical advice.</li>
                    <li style="margin: 3px 0;">P305+P351+P338+P315 - IF IN EYES : Rinse cautiously with water for several minutes. Remove contact lenses, if present and easy to do. Continue rinsing.</li>
                    <li style="margin: 3px 0;">P403 - Store in a well-ventilated place.</li>
                </ul> 
            </div> '''
            
    @api.model
    def _get_default_nrc_5_cac_html_text(self):
        return '''
            <div>
                <h6>
                    <strong>DANGER</strong>
                </h6>
                <p>
                    Extremely flammable gas. Contains gas under pressure; may explode if heated. Wear protective gloves, protective clothing, eye protection. Do not handle until all safety precautions have been read and understood. Do not breathe gas, vapours. Keep away from heat, hot surfaces, sparks, open flames and other ignition sources. No smoking. IF exposed or concerned: Get medical advice. Store in a well-ventilated place.
                </p>
            </div>
        '''
        
    @api.model
    def _get_default_nrc_5_cac_new_html_text(self):
        return '''
            <div>
                <h6>
                    <strong>DANGER</strong>
                </h6>
                <p>
                    Extremely flammable gas. Contains gas under pressure; may explode if heated. Keep away from heat, hot surfaces, sparks, open flames and other ignition sources. No smoking. Leaking gas fire: Do not extinguish unless leak can be stopped safely. In case of leakage, eliminate all ignition sources. Protect from sunlight. Store in a well ventilated place.
                </p>
            </div>
        '''
        
    @api.model
    def _get_default_nrc_3_cac_html_text(self):
        return '''
            <div>
                <h6>
                    <strong>Danger</strong>
                </h6>
                <p>
                    May cause or intensify fire; oxidiser, Contains gas under pressure; may explode if heated. Keep away from combustible materials, Keep valves and fittings free from oil and grease, In case of fire: Stop leak if safe to do so, Store in a well-ventilated place.
                </p>
            </div>
        '''
        
    @api.model
    def _get_default_nrc_3_cac_new_html_text(self):
        return '''
        
        '''
    
    components_ids = fields.One2many("product.components", "product_id", string="Components")
    useable_time_span = fields.Integer(string="Useable Time Span(Months)")
    nrc_imgs = fields.Selection(
        [('nrc1', 'GHS1'), ('nrc2', 'GHS2'), ('nrc3', 'GHS3'), ('nrc4', 'GHS4'), ('nrc5', 'GHS5'), ('nrc6', 'GHS6'),
         ('nrc7', 'GHS7'), ('nrc8', 'GHS8'), ('nrc9', 'GHS9'), ('nrc11', 'GHS11'), ('nrc12', 'GHS12'), ('nrc13', 'GHS13')], default='nrc1',
        string="GHS Logo")
    # https://spantech.odoo.com/web#id=1087&menu_id=554&cids=4%2C1%2C7%2C3%2C8%2C6%2C5%2C10%2C9%2C2&action=806&model=project.task&view_type=form
    nrc1 = fields.Html(string="GHS1", default=_get_default_nrc_1_2_html_text)
    nrc2 = fields.Html(string="GHS2", default=_get_default_nrc_1_2_html_text)
    nrc3 = fields.Html(string="GHS3", default=_get_default_nrc_3_html_text)
    nrc4 = fields.Html(string="GHS4", default=_get_default_nrc_4_5_6_html_text)
    nrc5 = fields.Html(string="GHS5", default=_get_default_nrc_4_5_6_html_text)
    nrc6 = fields.Html(string="GHS6", default=_get_default_nrc_4_5_6_html_text)
    nrc7 = fields.Html(string="GHS7", default=_get_default_nrc_7_html_text)
    nrc8 = fields.Html(string="GHS8", default=_get_default_nrc_8_9_html_text)
    nrc9 = fields.Html(string="GHS9", default=_get_default_nrc_8_9_html_text)
    nrc11 = fields.Html(string="GHS11", default=_get_default_nrc_11_html_text)
    nrc1_cac = fields.Html(string="GHS1 CAC", default=_get_default_nrc_1_cac_html_text)
    nrc4_cac = fields.Html(string="GHS4 CAC", default=_get_default_nrc_4_cac_html_text)
    nrc1_cac_new = fields.Html(string="GHS1 CAC New", default=_get_default_nrc_1_cac_new_html_text)
    nrc4_cac_new = fields.Html(string="GHS4 CAC New", default=_get_default_nrc_4_cac_new_html_text)
    nrc12 = fields.Html(string="GHS12", default=_get_default_nrc_12_html_text)
    nrc13 = fields.Html(string="GHS13", default=_get_default_nrc_13_html_text)
    nrc5_cac = fields.Html(string="GHS5 CAC", default=_get_default_nrc_5_cac_html_text)
    nrc5_cac_new = fields.Html(string="GHS5 CAC New", default=_get_default_nrc_5_cac_new_html_text)
    nrc3_cac = fields.Html(string="GHS3 CAC", default=_get_default_nrc_3_cac_html_text)
    nrc3_cac_new = fields.Html(string="GHS3 CAC New", default=_get_default_nrc_3_cac_new_html_text)
    

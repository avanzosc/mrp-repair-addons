# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class CrmClaim(models.Model):
    _inherit = "crm.claim"

    production_ids = fields.One2many(
        string="Production", comodel_name="mrp.production", inverse_name="claim_id"
    )
    production_count = fields.Integer(
        string="MOs counter", compute="_compute_production_count"
    )

    def _compute_production_count(self):
        for claim in self:
            claim.production_count = len(claim.production_ids)

    def action_view_productions(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("mrp.mrp_production_action")
        action["domain"] = expression.AND(
            [
                [("id", "in", self.production_ids.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        return action

# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        if "from_repair_order" not in self.env.context:
            return super().create(vals_list)
        for vals in vals_list:
            if "invoice_line_ids" in vals:
                repairs = self._get_distinct_repairs(vals.get("invoice_line_ids"))
                vals["invoice_line_ids"] = self._generate_creation_section_order(
                    repairs, vals.get("invoice_line_ids")
                )
        return super().create(vals_list)

    def _get_distinct_repairs(self, invoice_line_ids):
        repairs = self.env["repair.order"]
        for invoice_line in invoice_line_ids:
            if "repair_line_ids" in invoice_line[2]:
                repair_line = self.env["repair.line"].browse(
                    invoice_line[2].get("repair_line_ids")[0][1]
                )
                if repair_line.repair_id not in repairs:
                    repairs += repair_line.repair_id
            if "repair_fee_ids" in invoice_line[2]:
                repair_fee = self.env["repair.fee"].browse(
                    invoice_line[2].get("repair_fee_ids")[0][1]
                )
                if repair_fee.repair_id not in repairs:
                    repairs += repair_fee.repair_id
        return repairs.sorted(key=lambda r: r.name)

    def _generate_creation_section_order(self, repairs, invoice_line_ids):
        ordered_invoice_line_ids = []
        for repair in repairs:
            for invoice_line in invoice_line_ids:
                if "repair_fee_ids" in invoice_line[2]:
                    repair_fee = self.env["repair.fee"].browse(
                        invoice_line[2].get("repair_fee_ids")[0][1]
                    )
                    if repair_fee.repair_id == repair:
                        ordered_invoice_line_ids.append(invoice_line)
            for invoice_line in invoice_line_ids:
                if "repair_line_ids" in invoice_line[2]:
                    repair_line = self.env["repair.line"].browse(
                        invoice_line[2].get("repair_line_ids")[0][1]
                    )
                    if repair_line.repair_id == repair:
                        ordered_invoice_line_ids.append(invoice_line)
        return ordered_invoice_line_ids

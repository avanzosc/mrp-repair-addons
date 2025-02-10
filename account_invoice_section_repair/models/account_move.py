# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from pytz import timezone, utc

from odoo import _, api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        if "from_repair_order" not in self.env.context:
            return super().create(vals_list)
        my_invoice_line_ids = []
        repairs_treated = self.env["repair.order"]
        fee_pending = True
        for vals in vals_list:
            lines_vals = vals.get("invoice_line_ids")
            for line_vals in lines_vals:
                if "repair_line_ids" in line_vals[2]:
                    repair_line = self.env["repair.line"].browse(
                        line_vals[2].get("repair_line_ids")[0][1]
                    )
                    if repair_line.repair_id not in repairs_treated:
                        fee_pending = True
                        repairs_treated += repair_line.repair_id
                        my_invoice_line_ids = self._prepare_repair_info_section(
                            repair_line.repair_id, my_invoice_line_ids, False, True
                        )
                elif "repair_fee_ids" in line_vals[2]:
                    repair_fee = self.env["repair.fee"].browse(
                        line_vals[2].get("repair_fee_ids")[0][1]
                    )
                    print_repair_info = False
                    if (repair_fee.repair_id not in repairs_treated) or fee_pending:
                        if repair_fee.repair_id not in repairs_treated:
                            print_repair_info = True
                            repairs_treated += repair_fee.repair_id
                        fee_pending = False
                        my_invoice_line_ids = self._prepare_repair_info_section(
                            repair_fee.repair_id,
                            my_invoice_line_ids,
                            True,
                            print_repair_info,
                        )
                my_invoice_line_ids.append(line_vals)
            vals["invoice_line_ids"] = my_invoice_line_ids
        return super().create(vals_list)

    def _prepare_repair_info_section(
        self, repair, line_ids, is_operation, print_repair_info
    ):
        section_from_repair = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("section_from_repair", default=False)
        )
        if print_repair_info:
            vals = self._prepare_values_for_repair(repair)
            line_ids.append((0, 0, vals))
        if section_from_repair:
            my_name = _("OPERATIONS") if is_operation else _("PARTS")
            section_name = _("%(my_name)s - %(repair_name)s") % {
                "my_name": my_name,
                "repair_name": repair.name,
            }
            vals = {
                "name": section_name,
                "display_type": "line_section",
            }
            line_ids.append((0, 0, vals))
        return line_ids

    def _prepare_values_for_repair(self, repair):
        repair_name = self._get_repair_name_for_values(repair)
        vals = {
            "name": repair_name,
            "display_type": "line_section",
        }
        return vals

    def _get_repair_name_for_values(self, repair):
        date_repair = self._convert_to_local_date(repair.date_repair, repair.user_id)
        repair_name = _("Repair: %(repair)s, Date: %(date)s") % {
            "repair": repair.name,
            "date": date_repair,
        }
        if repair.lot_id:
            repair_name = _("%(repair_name)s, Num. Serie: %(lot)s") % {
                "repair_name": repair_name,
                "lot": repair.lot_id.name,
            }
        if repair.quotation_notes:
            quotation_notes = repair.convert_html_notes_to_char(repair.quotation_notes)
            repair_name = _("%(repair_name)s\n%(notes)s") % {
                "repair_name": repair_name,
                "notes": quotation_notes,
            }
        return repair_name

    def _convert_to_local_date(self, mydate, user):
        if not mydate:
            return ""
        tz = user.tz if user.tz else self.env.user.tz
        mydate = mydate.replace(tzinfo=utc)
        mydate = mydate.astimezone(timezone(tz)).replace(tzinfo=None)
        return datetime.strptime(str(mydate), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")

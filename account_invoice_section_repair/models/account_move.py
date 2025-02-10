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
        repairs_processed = self.env["repair.order"]
        pending_fee = True
        for vals in vals_list:
            updated_invoice_lines = []
            invoice_lines = vals.get("invoice_line_ids", [])
            for line_vals in invoice_lines:
                line_data = line_vals[2]
                if "repair_line_ids" in line_data:
                    repair_line = self.env["repair.line"].browse(
                        line_data["repair_line_ids"][0][1]
                    )
                    repair_order = repair_line.repair_id
                    if repair_order not in repairs_processed:
                        pending_fee = True
                        repairs_processed += repair_order
                        updated_invoice_lines = self._prepare_repair_info_section(
                            repair_order,
                            updated_invoice_lines,
                            add_fee=False,
                            print_repair_info=True,
                        )
                elif "repair_fee_ids" in line_data:
                    repair_fee = self.env["repair.fee"].browse(
                        line_data["repair_fee_ids"][0][1]
                    )
                    repair_order = repair_fee.repair_id
                    print_repair_info = False
                    if (repair_order not in repairs_processed) or pending_fee:
                        if repair_order not in repairs_processed:
                            print_repair_info = True
                            repairs_processed += repair_order
                        pending_fee = False
                        updated_invoice_lines = self._prepare_repair_info_section(
                            repair_order,
                            updated_invoice_lines,
                            add_fee=True,
                            print_repair_info=print_repair_info,
                        )
                updated_invoice_lines.append(line_vals)
            vals["invoice_line_ids"] = updated_invoice_lines
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

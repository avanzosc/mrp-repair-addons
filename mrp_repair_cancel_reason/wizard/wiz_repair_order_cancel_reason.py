# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class WizMrpRepairCancelReason(models.TransientModel):

    _name = "wiz.repair.order.cancel.reason"
    _description = "Ask a reason from the repair cancellation"

    reason_id = fields.Many2one(
        comodel_name="repair.order.cancel.reason",
        string="Reason",
        required=True,
    )

    def confirm_cancel(self):
        self.ensure_one()
        act_close = {"type": "ir.actions.act_window_close"}
        repair_ids = self.env.context.get("active_ids", False)
        repairs = (
            self.env["repair.order"]
            .browse(repair_ids)
            .filtered(lambda r: r.state != "cancel")
        )
        if not repairs:
            return act_close
        repairs.filtered(lambda r: not r.cancel_reason_id).write(
            {
                "cancel_reason_id": self.reason_id.id,
            }
        )
        repairs.action_repair_cancel()
        return act_close

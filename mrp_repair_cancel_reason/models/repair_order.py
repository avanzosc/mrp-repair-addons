# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, fields, models
from odoo.exceptions import UserError


class MrpRepair(models.Model):
    _inherit = "repair.order"

    cancel_reason_id = fields.Many2one(
        comodel_name="repair.order.cancel.reason",
        string="Reason for cancellation",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )

    def action_repair_cancel(self):
        if any(move.state == "done" for move in self.mapped("move_id")):
            raise UserError(
                _("You cannot cancel a repair order if it is already finished.")
            )
        if any(move.state == "done" for move in self.mapped("operations.move_id")):
            raise UserError(
                _("You cannot cancel a repair order with done stock moves.")
            )
        if any(repair.state == "done" for repair in self):
            raise UserError(_("You cannot cancel a completed repair order."))
        if not all(repair.cancel_reason_id for repair in self):
            action = self.env["ir.actions.actions"]._for_xml_id(
                "mrp_repair_cancel_reason.action_repair_order_cancel_with_reason"
            )
            action["context"] = dict(self._context, create=False)
            return action
        return super().action_repair_cancel()

    def action_repair_cancel_draft(self):
        if self.filtered(lambda repair: repair.state != "cancel"):
            raise UserError(_("Repair must be canceled in order to reset it to draft."))
        self.write(
            {
                "cancel_reason_id": False,
            }
        )
        return super().action_repair_cancel_draft()


class MrpRepairCancelReason(models.Model):
    _name = "repair.order.cancel.reason"
    _description = "Repair Cancel Reason"

    name = fields.Char(
        string="Reason",
        required=True,
        translate=True,
    )

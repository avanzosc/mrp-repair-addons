# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    def _get_order_type(self):
        return self.env['repair.order.type'].search([], limit=1)

    name = fields.Char(default="/")
    type_id = fields.Many2one(
        comodel_name='repair.order.type',
        string='Type',
        default=_get_order_type,
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]}
    )

    @api.onchange('type_id')
    def onchange_location_id(self):
        if self.type_id and self.type_id.reparation_location_id:
            self.location_id = self.type_id.reparation_location_id.id

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/' and vals.get('type_id'):
            repair_type = self.env['repair.order.type'].browse(vals['type_id'])
            if repair_type.sequence_id:
                vals['name'] = repair_type.sequence_id.next_by_id()
        return super(RepairOrder, self).create(vals)

    def write(self, vals):
        if vals.get("type_id"):
            repair_type = self.env["repair.order.type"].browse(vals["type_id"])
            if repair_type.sequence_id:
                for record in self:
                    if (
                        record.state in {"draft"}) and (
                            record.type_id.sequence_id != (
                                repair_type.sequence_id)):
                        new_vals = vals.copy()
                        new_vals["name"] = repair_type.sequence_id.next_by_id()
                        super(RepairOrder, record).write(new_vals)
                    else:
                        super(RepairOrder, record).write(vals)
                return True
        return super().write(vals)

# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestRepairValidate(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestRepairValidate, cls).setUpClass()
        cls.repair_model = cls.env['repair.order']
        cls.repair = cls.repair_model.search([], limit=1)

    def test_repair_validate(self):
        self.repair.action_task_end()
        self.assertEqual(self.repair.finished_task, True)
        self.repair.action_cancel_validation()
        self.assertEqual(self.repair.finished_task, False)
        self.assertEqual(self.repair.state, 'under_repair')

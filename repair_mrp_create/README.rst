.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=================
Repair MRP Create
=================

This module links repair orders with manufacturing, allowing to create a
manufacturing order directly from a repair order.

It adds the following features:

- A **Eligible in repairs** checkbox on bills of materials.
- A **Bill of Materials** field on repair orders, limited to the bills of
  materials marked as eligible in repairs.
- A **Create MO** button on the repair order that creates a manufacturing
  order, taking the final product from the repair's bill of materials and a
  quantity of 1.
- The created manufacturing order keeps a link back to the originating repair
  order, and the repair order shows the related manufacturing orders.
- The repair order is shown, when available, in the operations (work orders)
  and operation times (productivity) tables.

Usage
=====

To create a manufacturing order from a repair order:

1.  Go to *Manufacturing > Products > Bills of Materials* and check
    **Eligible in repairs** on the bills of materials you want to make
    available in repairs.
2.  Go to *Repairs* and open or create a repair order.
3.  In the **Bill of Materials** field, select one of the bills of materials
    marked as eligible in repairs.
4.  Press the **Create MO** button. A manufacturing order is created for the
    final product of the bill of materials, with a quantity of 1, and linked
    back to the repair order.
5.  Use the **Manufacturing Orders** smart button on the repair order to open
    the related manufacturing orders.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/avanzosc/mrp-repair-addons/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* AvanzOSC

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Aner Arregi <aneravanzosc@gmail.com>

Maintainers
-----------

This module is maintained by AvanzOSC.

This module is part of the `avanzosc/mrp-repair-addons <https://github.com/avanzosc/mrp-repair-addons/tree/18.0/repair_mrp_create>`_ project on GitHub.

You are welcome to contribute.

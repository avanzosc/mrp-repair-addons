.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===============================
Repair Customer Product Warning
===============================

This module extends the Repair application by adding warning messages on **customers** and **products** in Repair Orders.

**Features**

- Add a **Repair Warning** field on customers (`res.partner`).
  - Define warning or blocking messages to be displayed when the customer is selected in a repair order.
- Add a **Repair Line Warning** field on products (`product.template`).
  - Define warning or blocking messages to be displayed when the product is added to a repair line or is selected in a repair order.
- System setting in **Repair Configuration** to enable/disable warnings.
- Warning messages can be:
  - **No Message**: nothing happens.
  - **Warning**: a message is displayed in a popup.
  - **Blocking Message**: selection is cancelled and a blocking message is displayed.

**Usage**

1. Go to **Settings > General Settings > Repairs** and activate *Repair Order Warnings*.
2. On a customer form, set a **Repair Warning** and enter a message.
3. On a product form, set a **Repair Line Warning** and enter a message.
4. When creating a repair order:
   - Selecting a customer with a warning will trigger a popup message.
   - Adding a product with a warning will trigger a popup message.

**Example**

- If a customer is marked with a **Blocking Repair Warning**, they cannot be selected on a repair order.
- If a product has a **Repair Line Warning**, a popup will warn the user when the product is selected or added to a repair line.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/mrp-repair-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>

* Lucía Echeverría <luciaecheverria@avanzosc.es>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the AGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.


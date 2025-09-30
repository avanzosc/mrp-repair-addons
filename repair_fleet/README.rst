.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

============
Repair Fleet
============

This module extends **Repair Orders** in Odoo 14 with the following features:

* In product categories, a new checkbox **"Repairable"**.
* In repair orders, the field **Product to Repair** is restricted to products
  whose category has the "Repairable" checkbox enabled.
* The label of the **Lot/Serial Number** field is changed to
  **"Lot/Serial Number (License Plate)"**.
* A new **Vehicle** section is added in repair orders with:

  - Vehicle (related from the lot/serial number).
  - Brand, Model, License Plate, and Chassis Number (readonly, related to the vehicle).
  - Odometer (Km).
  - Fuel Level (selection: 1/4, 1/2, 3/4, Full).

* When closing the repair, if Odometer is set and a Vehicle is linked,
  an **Odometer line** is automatically created for that vehicle.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/mrp-repair-addons/issues>`_.  
In case of trouble, please check there if your issue has already been reported.  
If you spotted it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Ane Gurruchaga <aneavanzosc@gmail.com>
* Ana Juaristi <ajuaristio@gmail.com>

Do not contact contributors directly about support or help with technical issues.

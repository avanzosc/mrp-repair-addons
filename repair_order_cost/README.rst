.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================
Repair order cost
=================

* In repair "Services", new field "Operations cost", with calculation quantity *
  product cost (standard_price).
* In repair "Parts", new computed field "Material cost", which depends on the
  cost of its associated move lines.
* In "Repair Order" new fields: "Material cost", "Operations cost", and
  "Total repair cost".
* To view these costs, the user must be in the new group
  "Show repair order costs".

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/mrp-repair-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted it
first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
* Ana Juaristi <ajuaristio@gmail.com>

Do not contact contributors directly about support or help with technical issues.

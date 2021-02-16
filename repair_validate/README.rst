.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============
Repair validate
===============

* Add an invisible / internal boolean "Task completed" field and a button
  "END JOB" visible to all repair users, only in the
  if the status is "in process of repair", that is, it has been
  repair started.
* By pressing the "END TASK" button, mark the internal check "Task
  completed ".
* Add a permission group "Allowed to close repairs", that is, only
  users who have this permissions would have visible and could press the button
  "Finish repair" (this group must be able to access all the
  state)
* The group that does not have "allow close repairs" permissions can only see
  and have access to the Repair Orders that are in "Confirmed" status,
  or "Under repair"

* So that a user with these permissions can press the button "finish
  repair ", the check" Task completed "must be set to True, if not, or
  well the button is not visible to anyone. It would not show the button "finish
  repair ”for any user until the“ Task completed ”check is
  TRUE. (so all users see the same "workflow", the only thing that
  operators cannot go all the way)
* Add in the menu a filter / grouping by the field "Task completed".
* There would also be a button "cancel validation" that what it does is put the
  check to false and return to the previous state of the workflow (to return to
  status "under repair" and the operator has access to the order) In such a way
  that operators can include what is missing in the repair and return to
  "Finished work "
* Once closed "for real" it will not be possible to modify or reopen the
  repair. (that is, as Odoo does by default) 

Bug Tracker
===========


Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.

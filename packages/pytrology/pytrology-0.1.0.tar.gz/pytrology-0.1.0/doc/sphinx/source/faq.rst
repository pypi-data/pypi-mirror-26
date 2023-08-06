.. include:: project-links.txt
.. include:: abbreviation.txt

.. _user-faq-page:

==========
 User FAQ
==========

How to get help or report an issue ?
------------------------------------

.. There is no mailing list or forum actually, so you can either contact me or fill an issue on Github.

If you want to **discuss or ask questions on PyMetrology**, you can subscribe and post messages on the
**PyMetrology User** mailing list.

There is actually three lists running on Google Groups (*):

`User List <https://groups.google.com/forum/#!forum/pymetrology-user>`_
  List for PyMetrology users
`Announce List <https://groups.google.com/forum/#!forum/pymetrology-announce>`_
  List for announcements regarding PyMetrology releases and development
`Devel List <https://groups.google.com/forum/#!forum/pymetrology-devel>`_
  List for developers of PyMetrology

**If you encounter an issue, please fill an issue** on the `Issue Tracker <https://github.com/FabriceSalvaire/PyMetrology/issues>`_.

(*) Despite Google Groups has many drawbacks, I don't have actually enough resources to run GNU Mailman or
Discourse on my own IT infrastructure.

How to typeset :code:`u_kΩ` or :code:`u_μV` in Python code ?
------------------------------------------------------------

There is three solutions if you don't have these Unicode characters available on your keyboard. The
first one, is to use the ASCII alternative: :code:`u_kOhm` or :code:`u_uV.`.  The second one, is to
define macros on your favourite editor.  The last one, is to customise your keyboard settings (on Linux look at https://www.x.org/wiki/XKB/).

Is unit API well tested ?
-------------------------

**Unit API is an ongoing work.  You must use it with caution since it can be buggy or incomplete.**

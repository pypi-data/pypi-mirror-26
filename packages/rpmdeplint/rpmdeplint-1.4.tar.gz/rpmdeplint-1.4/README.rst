rpmdeplint
==========

Rpmdeplint is a tool to find errors in RPM packages in the context of their
dependency graph.

Requirements
------------

* Python 2.7

External Dependencies
---------------------

In order to run the tool, the following pre-requisites need to be installed:

* rpm, rpm-python
* librepo, python-librepo
* hawkey, python-hawkey

For development and tests:

* sphinx
* `rpmfluff <https://pagure.io/rpmfluff>`_
* glibc-devel.i686 and libgcc.i686, for building 32-bit binaries

Project Links
-------------

* `Source code on Pagure <https://pagure.io/rpmdeplint>`__
* `File a bug <https://bugzilla.redhat.com/enter_bug.cgi?product=rpmdeplint>`__
  or `view open bugs <https://bugzilla.redhat.com/buglist.cgi?product=rpmdeplint&bug_status=__open__>`__
* For feedback and discussion join #beaker on irc.freenode.net.
* We use `Gerrit <https://gerrit.beaker-project.org>`_ for code review. Patches welcome!
* `Documentation <https://rpmdeplint.readthedocs.io>`_

Using
-----

A user guide is provided by the man(1) page shipped with this tool::

  man rpmdeplint

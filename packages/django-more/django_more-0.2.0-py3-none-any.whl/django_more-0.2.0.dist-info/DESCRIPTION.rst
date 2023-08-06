django-more
===========

| A collection of Django patches and extensions to give more of the
  features and functionality that I want or expect from Django.
| *Currently aimed only at Django 1.11*

django\_more
------------

Extras for Django that do not require any patching and can be used
directly. \* *django\_more.storages* \* *django\_more.PartialIndex* \*
*django\_more.HashField* \* *django\_more.OrderByField*

django\_cte
-----------

Patches Django to add CTE based functionality. \*
django\_cte.patch\_cte()

| **Not included in distributions until out of WIP state**
| *Placing django\_cte into Django INSTALLED\_APPS will automatically
  invoke patch\_cte()*

django\_enum
------------

Patches Django to add EnumFields, with enum state information in
migrations to allow for consistent migrations compatible with postgres
and mysql. \* django\_enum.EnumField \* django\_enum.enum\_meta \*
django\_enum.patch\_enum()

*Placing django\_enum into Django INSTALLED\_APPS will automatically
invoke patch\_enum()*

django\_types
-------------

Patches Django to add support for custom database types to be used
within migrations. \* django\_types.patch\_types()

*To avoid additional dependencies in INSTALLED\_APPS, apps adding types
requiring this should check for ProjectState.add\_type() support, and if
not present apply this with patch\_types()*

patchy
------

A class based monkey patching package used by the other django\_more
packages to apply their patches in a consistent and safe manner that is
hopefully less fragile to Django core changes. \* patchy.patchy() \*
patchy.super\_patchy()

Version History
===============

| *0.2.0*
| Added documentation for *django\_more* features in *README*.
  Refactored *django\_more.fields* into sub-module. Added:
| \* django\_more.OrderByField

| *0.1.1*
| Bugfix to include *django\_types* in distribution as necessary for
  *django\_enum*.

| *0.1.0*
| Initial release without *django\_cte*.
| Added:
| \* django\_enum.EnumField \* django\_more.PartialIndex \*
  django\_more.HashField \* django\_more.storages



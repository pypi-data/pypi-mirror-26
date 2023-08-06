Changelog
=========


2.0.8 (2017-11-20)
------------------

New:

- Update diazo and js


2.0.7 (2017-11-08)
------------------

Fixed:

- Drop the theme "back-to-portal" on screen help.
  Diazo will set the corrent one from the theme when replacing the site logo.


2.0.6 (2017-10-23)
------------------

New:

- Update diazo and js to fix IE11 issues


2.0.5 (2017-10-11)
------------------

New:

- Update diazo and js


2.0.4 (2017-10-11)
------------------

New:

- Update diazo and js


2.0.3 (2017-09-22)
------------------

New:

- Update diazo and js


2.0.2 (2017-09-20)
------------------

New:

- Update diazo


2.0.1 (2017-09-09)
------------------

New:

- New js build


2.0.0 (2017-09-01)
------------------

New:

- The latest prototype uses patternslib 3 and webpack to bundle
  the javascrcipt resources.


1.3.28 (2017-08-29)
-------------------

Added:

- A diazo rule to properly render the on screen help toggle button
  (Refs. Syslab #15824).
  [Alessandro Pisa]


1.3.27 (2017-08-29)
-------------------

Fixes:

- Include the patch from
  https://github.com/Patternslib/Patterns/pull/510
  that fixes a collision between pat-modal and pat-collapsible.

New:

- Updated the theme
  [Alessandrop Pisa]


1.3.26 (2017-07-24)
-------------------

- Prepare the diazo rules for the help bubbles
- Understand the is_modal_panel view attribute
- Added rules for panels
- Updated the js release
- Updated diazo [Alessandro Pisa]


1.3.25 (2017-06-13)
-------------------

- Updated bundle and diazo theme [Alessandro Pisa]


1.3.24 (2017-06-05)
-------------------

- Updated bundle and diazo theme [Alessandro Pisa]


1.3.23 (2017-05-30)
-------------------

- Clean up annotorius [Alessandro Pisa]
- Fix Makefile [Alessandro Pisa]
- Via Proto: Updated Blue theme for Quaive, plus new Quaive logo [Wolfgang Thomas]
- Back to blue [Alessandro Pisa, Wolfgang Thomas]
- Simplify the diazo rules [Alessandro Pisa]


1.3.21 (2017-05-12)
-------------------

- Copy the lang attribute of the html element [Alessandro Pisa]
- Updated js bundle [Alessandro Pisa]


1.3.21a1 (2017-05-09)
---------------------

- Simplify the diazo rules and copy the title tag from Plone
  (see quaive/ploneintranet#1027) [Alessandro Pisa]


1.3.20 (2017-05-08)
-------------------

- Update CSS [Alessandro Pisa]


1.3.20a1 (2017-04-28)
---------------------

- Simplify diazo rules [Alessandro Pisa]
- Updated theme and bundle [Alessandro Pisa]


1.3.19 (2017-03-29)
-------------------

- Updated bundle [Alessandro Pisa]


1.3.18 (2017-03-07)
-------------------

- Updated Proto [Alessandro Pisa]


1.3.17 (2017-02-21)
-------------------

- Do not render the Plone toolbar when we do not need it [Alessandro Pisa]


1.3.16 (2017-02-01)
-------------------

- Nothing changed yet.


1.3.15 (2017-01-18)
-------------------

- Nothing changed yet.


1.3.14 (2016-12-20)
-------------------

* Drop the alpha [Guido A.J. Stevens]
* Update changelog [Guido A.J. Stevens]
* ignore auto-backups [Guido A.J. Stevens]
* Don't show a no-op global settings link [Guido A.J. Stevens]
* update proto [Alexander Pilz]
* fixurl doesn't like the if statements on the same line [Alexander Pilz]
* Fix regression for Library details page (ported from ikath) See https://git.syslab.com/ikath/quaive.resources.ikath/commit/6ffe0
* Disable q.r.p. resources in Barceloneta fixes https://github.com/quaive/ploneintranet/issues/876 [Guido A.J. Stevens]
* update proto [Alexander Pilz]
* update proto [Alexander Pilz]
* Let's be Quaive [Alessandro Pisa]
* update js bundle [Alexander Pilz]
* Back to development: 1.3.0a14 [Wolfgang Thomas]


1.3.0a13 (2016-11-07)
---------------------

- simplify the rules for the whole password reset story. This implies that all
  relevant templates are overriden in ploneintranet, see quaive/ploneintranet#870
  [Wolfgang Thomas]

- Support newsitem view [Guido Stevens]

- Add 16x9 placeholder for news magazine [Guido Stevens]


1.3.0a12 (2016-11-01)
---------------------

* Preparing release 1.3.0a12 [Alexander Pilz]
* Update diazo [Alexander Pilz]
* Back to development: 1.3.0a12 [Alexander Pilz]


1.3.0a11 (2016-10-27)
---------------------

* Preparing release 1.3.0a11 [Alexander Pilz]
* update diazo [Alexander Pilz]
* Back to development: 1.3.0a11 [Alessandro Pisa]


1.3.0a10 (2016-10-26)
---------------------

* Catch urls like ++add++ptype (used in tests) [Alessandro Pisa]
* Updated bundle so that redactor triggers the change event. Needed for autosave [Alexander Pilz]
* new bundle where redactor triggers the change event [Alexander Pilz]
* Fix fallback rules to only catch if a visual portal wrapper is present [Alexander Pilz]
* updated diazo [Alexander Pilz]
* added rule for posts [Alexander Pilz]
* Rulefix for calendar [Alexander Pilz]
* Rules for calendar [Alexander Pilz]
* update diazo [Alexander Pilz]
* Updated proto [Alexander Pilz]
* Added default user icons [Alexander Pilz]
* Also copy defaultusers [Alexander Pilz]
* Remove empty.html fallback [Cillian de Roiste]
* update diazo [Alexander Pilz]
* Move main_template test over from ploneintranet.theme and fix plone.app.blocks dependency [Guido A.J. Stevens]
* Move dependencies and registry setup/uninstall from theme refs https://github.com/quaive/ploneintranet/commit/dba9d8b09b10ac15a1f3e6274d11cd0437ae1fdd [Guido A.J. Stevens]
* Audit zope.Public refs https://github.com/quaive/ploneintranet/issues/765 [Guido A.J. Stevens]
* make diazo [Alessandro Pisa]
* Consolidate news rules [Guido A.J. Stevens]
* Added empty placeholder app icon [Manuel Reinhardt]
* Don't depend on section ids (controlled by content editors) [Guido A.J. Stevens]
* Reorganize diazo rules [Guido A.J. Stevens]
* Update some outdated rules [Guido A.J. Stevens]
* Hook up news publisher template [Guido A.J. Stevens]
* Hook up news app, refs #337 [Guido A.J. Stevens]
* Back to development: 1.3.0a10 [Guido A.J. Stevens]


1.3.0a9 (2016-09-16)
--------------------

* Update changelog [Guido A.J. Stevens]
* Update proto from c2ab9deba47758a383d029f8541c236b6990509 [Guido A.J. Stevens]
* Give a preview to this theme [Alessandro Pisa]
* Back to development: 1.3.0a9 [Alexander Pilz]

1.3.0a8 (2016-09-14)
--------------------

- Update proto [pilz]
- Update bundle which now cleans up the moment-timezone messup, reducing size
  [pilz]
- Include rule for calendar app
  [pilz]

1.3.0a7 (2016-09-12)
--------------------

* Fix manifest [Guido A.J. Stevens]
* Update changelog [Guido A.J. Stevens]
* Fix regression that broke workspace subclasses [Guido A.J. Stevens]
* actually write converted files to the diazo dir [Alexander Pilz]
* Also view the mails [Alessandro Pisa]
* update bundle [Alexander Pilz]
* Back to development: 1.3.0a7 [Alexander Pilz]


1.3.0a6 (2016-08-31)
--------------------

- Prototype Style update


1.3.0a5 (2016-08-31)
--------------------

- Diazo rules update


1.3.0a4 (2016-08-29)
--------------------

- Prototype Style update


1.3.0a3 (2016-08-25)
--------------------

- Fix merge regression that damaged 85c37862a8e2 [Guido A.J. Stevens]

1.3.0a2 (2016-08-25)
--------------------

- Shell change

1.3.0a1 (2016-08-22)
--------------------

- Initial version implementing the shell change

1.2.5 (2016-08-19)
------------------

- Monkey scroll fix directly into bundle. See https://github.com/Patternslib/Patterns/pull/455 [Guido A.J. Stevens]


1.2.4 (2016-08-18)
------------------

Extra release to verify that 1.2.3. was not a brownbag release.

* fix postrelease typo [Guido A.J. Stevens]


1.2.3 (2016-08-18)
------------------

* New bundle with the actual inject API change, finally [Guido A.J. Stevens]
* Update Makefile to remove old releases, update symlinks to actually point to LATEST [Guido A.J. Stevens]
* Revert "Updated from prototype" [Guido A.J. Stevens]
* Fix Makefile to handle bundle again, add new bundle [Alexander Pilz]
* new bundle [Alexander Pilz]
* update patternslib to include https://github.com/Patternslib/Patterns/pull/452/commits/35e59cba63aa6e51a35b1fe4a0df79d391462849
* Back to development: 1.2.3 [Alexander Pilz]


1.2.2 (2016-08-18)
------------------

- Pull in another Patternslib:inject_delay [Guido A.J. Stevens]


1.2.1 (2016-08-10)
------------------

- Pull in Patternslib:inject_delay [Guido A.J. Stevens]


1.2.0 (2016-08-08)
------------------

* Remove FIXME, ongoing work in quaive/ploneintranet:update-proto will fix that [Guido A.J. Stevens]
* Hook up global messaging counter + link [Guido A.J. Stevens]
* Hook up messaging [Guido A.J. Stevens]
* Sort uninstaller downwards [Guido A.J. Stevens]
* Promote theme profile installer in GS/QI UI [Guido A.J. Stevens]
* Back to development: 1.2.0a4 [Guido A.J. Stevens]


1.2.0a3 (2016-08-01)
--------------------

* Remove circular ploneintranet <-> resources dependency, disable autoinclude [Guido A.J. Stevens]
* Modernize setup.py author pointers [Guido A.J. Stevens]
* Theme updated to pull in mail content type related stuff [Alessandro Pisa]
* Updated the Makefile [Alessandro Pisa]


1.2.0a2 (2016-07-27)
--------------------

- Modified the rules.xml as in quaive/ploneintranet#510 [ale-rt]


1.2.0a1 (2016-07-26)
--------------------

- Updated static folder after quaive/ploneintranet#476 [ale-rt]


1.2.0a0 (2016-07-25)
--------------------

- Inital release [ale-rt]

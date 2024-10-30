odoo-openupgrade-wizard changes
*******************************

This file compiles releases and changes made in
``odoo-openupgrade-wizard``.

.. towncrier release notes start

odoo-openupgrade-wizard 1.0.3 (2024-10-09)
==========================================

Bugfixes
--------

- Fix crash when building container fails.
- Make odoo openupgrade wizard working in the following combination:
  Odoo version <= 12 + Postgresql version >= 14
- New fix for error that append randomly when removing a container.


Documentation
-------------

- Add towncrier and newsfragments info in dev documentation.
- Improve the README.md file, hightlighting code section.
- Update contributors list until October 2024


Misc
----

- Update of python libraries version, using ``poetry update``.

  * Removing incremental (22.10.0)
  * Updating attrs (23.2.0 -> 24.2.0)
  * Updating certifi (2024.2.2 -> 2024.8.30)
  * Updating filelock (3.13.2 -> 3.16.1)
  * Updating idna (3.6 -> 3.10)
  * Updating packaging (24.0 -> 24.1)
  * Updating platformdirs (4.2.0 -> 4.3.6)
  * Updating pygments (2.17.2 -> 2.18.0)
  * Updating pyyaml (6.0.1 -> 6.0.2)
  * Updating tomli (2.0.1 -> 2.0.2)
  * Updating typing-extensions (4.10.0 -> 4.12.2)
  * Updating urllib3 (2.2.1 -> 2.2.3)
  * Updating zipp (3.18.1 -> 3.20.2)
  * Updating argcomplete (3.2.3 -> 3.5.1)
  * Updating astroid (3.1.0 -> 3.3.5)
  * Updating coverage (7.4.4 -> 7.6.1)
  * Updating dill (0.3.8 -> 0.3.9)
  * Updating gitpython (3.1.42 -> 3.1.43)
  * Updating jinja2 (3.1.3 -> 3.1.4)
  * Updating requests (2.31.0 -> 2.32.3)
  * Updating rich (13.7.1 -> 13.9.2)
  * Updating setuptools (69.2.0 -> 75.1.0)
  * Updating tomlkit (0.12.4 -> 0.13.2)
  * Updating virtualenv (20.25.1 -> 20.26.6)
  * Updating docker (7.0.0 -> 7.1.0)
  * Updating plumbum (1.8.2 -> 1.9.0)
  * Updating pylint (3.1.0 -> 3.3.1)
  * Updating towncrier (23.11.0 -> 24.8.0)


odoo-openupgrade-wizard 1.0.2 (2024-10-06)
==========================================

Bugfixes
--------

- Added a check to ensure the source exists before database operations,
  preventing the destination from being dropped if the source is missing.
  (check-db-exist-before-operations)
- Fix error that append randomly when removing a container. (container-removal)
- Require to specify the --database arg for every command that needs it
  (install_from_csv, psql, run, generate_module_analysis)
  (require-database-arg)


odoo-openupgrade-wizard 1.0.1 (2024-10-01)
==========================================

Features
--------

- Avoid to crash if postgresql-version is not set, adding prompt option
  and add extra text to mention postgresql version constraints.
  (postgresql-version-prompt)


Misc
----

- Refactor to simplify configuration_version_dependant.py file.
  (version-simplification)


odoo-openupgrade-wizard 1.0.0 (2024-09-30)
==========================================

Features
--------

- Add option ``p`` (SQL format) allowing use from ``--database-format`` CLI.
  This allows you to restore database in SQL format (used by odoo full backup)
  (add-sql-option-for-database-format-cli)


Bugfixes
--------

- Allow to run multiple `post-*.py` script for each steps.
  (allow-run-multiple-post-scripts)
- Fix metadata of the python package on PyPI. (fix-package-metadata)


odoo-openupgrade-wizard 0.7.0 (2024-05-02)
==========================================

Features
--------

- Add ``--config-file`` and ``--modules-file`` CLI options. This allows to use
  different files than the default ones. This is useful when using the same
  environment for different databases. (add-config-file-cli-option)
- Add database name to container name and publish Docker ports only when needed
  to allow to upgrade multiple databases in parallel.
  (allow-to-upgrade-multiple-databases-in-parallel)
- Drop support for python version < 3.9. Update dependencies and fix some
  issue liked to that. (drop-old-python-support)
- Add a new option ``--postgresql-version`` in ``oow init`` command to
  define the version of the postgresql image to be used for the project.
  (option-postgresql-version)
- Factorize code. Allways set --log-level=DEBUG in tests.
  (set-log-level-debug-default-in-cli_runner_invoke)


Bugfixes
--------

- Allow hyphen-minus character in database names.
  (allow-minus-in-database-names)


odoo-openupgrade-wizard 0.6.0 (2024-03-20)
==========================================

Features
--------

- Add ``dropdb`` command to easily delete database and filestore of existing
  Odoo databases in PostgreSQL container. (add-dropdb)
- With ``install-from-csv`` and the ``--with-demo / --without-demo``, you
  can control if the created database will be populated with demo data or
  not. (add-install-from-csv-demo)
- Add ``restoredb`` command to restore database and filestore in the
  PostgreSQL container. (add-restoredb)
- Add ``--update-modules`` option to ``run`` command. (imp-run-update-modules)
- ``run`` and ``upgrade`` command are now harmonized with the option
  ``--with-demo / --without-demo``. By default demo data is always false.
  (imp-run-upgrade)


Bugfixes
--------

- ``copydb`` now copy also the filestore of the database. (copydb-filestore)
- Fix warning message for ``estimate-workload`` command.
  (fix-estimate-workload-warning-message)
- Fix getting url on apps.odoo.com that prevent from running
  ``estimate-workload`` command. (fix-getting-url)
- Fix crash when a addons-path directory does not contain modules.
  Directory that does not contains odoo modules are now removed from
  addons-path option of odoo. (fix-repo)


Misc
----

- ci-improvement

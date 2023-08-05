=======
History
=======

v0.0.5 / 2017-10-25
===================

  * updated docs
  * Makefile: pull-req-check aliased to test-all
  * flake8
  * make test-all now tests docs build

v0.0.4 / 2017-10-25
===================

  * travis tests now passing
  * changed pypi deploy target to 3.7
  * utils/loaders.py: added file (smart table loaders)
  * track some xls files for tests

v0.0.3 / 2017-10-24
===================

  * Makefile: experimenting with install structure
  * test_coordinator_data_tasks.py: removed useless test
  * cli.py: added join subcommands
  * requirements.dev.pip.txt: mypy lives here now
  * docs/index.rst: fixed too few `==` under title
  * docs/conf.py: upgraded auto-build code
  * left_join.py: more log entries
  * moved recommonmark req to requirements.pip.txt
  * got tox to work
  * Makefile: experimenting with install structure
  * MANIFEST.in: add req files to allow tox to work
  * flake8
  * removed setup and test specific req files
  * README.rst: fixed badge address errors
  * fix repo in travis ci setup

v0.0.2 / 2017-10-23
===================

  * prelim tests
  * allow from coordinator_data_tasks import commands
  * travis ci setup

v0.0.1 / 2017-10-23
===================

  * setup.py: update metadata (language support)
  * configure tox
  * Makefile: formatting
  * Makefile: py.test -> pytest
  * setup.py: pick up reqs from req.txt files
  * setup.cfg: ignore some errors
  * Makefile: upgraded help, supported conda install
  * requirements.dev.txt: unpin for now
  * added commands pkg
  * added utils pkg
  * added extra requirements subfiles (pip,setup,etc)
  * ignore binary document extentions
  * ignore vscode and mypy_cache

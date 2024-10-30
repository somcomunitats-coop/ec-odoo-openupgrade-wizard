# Installation to develop

## Basic installation

```
git clone https://gitlab.com/odoo-openupgrade-wizard/odoo-openupgrade-wizard/
cd odoo-openupgrade-wizard
virtualenv env --python=python3
. ./env/bin/activate
poetry install
```

``odoo-openupgrade-wizard`` commands are now available in your virutalenv.

## Advanced installation

If you want to use this library without installing anything in your
system, execute the following steps, otherwise, go to 'Installation' part.

1. Run a docker container:

``docker run -it ubuntu:focal``

2. Execute the following commnands

```

apt-get update
apt-get install git python3 python3-pip python3-venv

python3 -m pip install --user pipx
python3 -m pipx ensurepath

su root

pipx install virtualenv
pipx install poetry
```

# Run tests

## Via pytest (simple)

This will run tests only for the current ``python3.X`` version.

(in your virtualenv)
```
poetry run pytest --cov odoo_openupgrade_wizard --verbosity=2 --exitfirst
```

## Via Tox (advanced)

This will run tests for all the python versions put in the ``tox.ini`` folder.

(in your virtualenv)
```
tox
```

Note : you should have all the python versions available in your local system.


```
sudo apt-get install python3.6  python3.6-distutils
sudo apt-get install python3.7  python3.7-distutils
sudo apt-get install python3.8  python3.8-distutils
sudo apt-get install python3.9  python3.9-distutils
```

## Via Gitlab Runner locally


```
# Install tools
pipx install gitlabci-local

# Run new available command
gitlabci-local
```

# Debugging

Some docker command could help you when using / developping this tools.

**Enter the postgres container**

docker exec -it POSTGRES_CONTAINER_NAME /bin/bash

# Contribute

## Provide newsfragments in your merge requests

If you propose a merge request, please add a newsfragments with it.

A newsfragment is a small file describing what is done in the merge
request. The file has a extension (e.g. `.feature`, `.bugfix`, etc) that
describe witch type of modification you are doing. This newsfragment
file will populate the CHANGES.rst file for the next release.
Documentation and the full list of default available extension can be
found [here](https://towncrier.readthedocs.io/en/stable/tutorial.html#creating-news-fragments).

Newsfragments must be put in the `newsfragments` directory at the root
of the project. You can install `towncrier` via `pipx install
towncrier`.

The newsfragments file will be processed with `towncrier` by the
maintainers during the release process.

Use `towncrier create --help` to see the available extension for the
newsfragement files. The name of the file can be a number referring an
issue of the project or a
[slug](https://en.wikipedia.org/wiki/Clean_URL#Slug) that start with
a `+` symbol.

This is a example of newsfragments.

`newsfragments/+sub-command-cowsay.feature`:
```
Adds a new subcommand `cowsay` to allow poeple to speak like a cow.
```

## Add python dependencies

If you add new dependencies, you have to:

- add the reference in the file ``pyproject.toml``

- run the following command in your virtualenv : ``poetry update``

## Release on Gitlab and publish on PyPI

Building, releasing and publishing a new version works with tags.

Tags that trigger a build and a publication on PyPI must have a name
equal to the version of the program found in `pyproject.toml`.

Tags that matches an change in major, minor or patch version will
trigger a release on gitlab.

Tags that are alpha, beta, pre-release, etc does not trigger a release
on gitlab, but they trigger a publication on PyPI.

Before creating a tag, ensure that the version of the program is
updated. To update the program version you can use the command:

```
poetry version {major,minor,patch}
```

Ensure that the `CHANGES.rst` file contains information about this new
release, if it is a major, minor or patch release. For alpha, beta, etc
release information will be published with the next major, minor or
patch release.

Then push a commit with the version and the changlog updated on the main
branch.

When everything is good on the main branch and that tests succeed,
create a new tag with the same name as the version in `pyproject.toml`
file. Tags can be created via Code > Tags > New tag.

To see if the publication on PyPI and the release on gitlab were done
correctly, go in Build > Pipelines. You will find a pipeline for the tag
you just created.


# Understanding the library

## Tools to understand

The library is using many tools. It is recommanded to understand that tools
to contribute to that project:

* Docker (https://www.docker.com/)
* Gitlab CI (https://docs.gitlab.com/ee/ci/quick_start/index.html)
* openupgrade project (https://github.com/oca/openupgrade) and related openupgradelib (https://github.com/oca/openupgradelib)
* poetry (https://python-poetry.org/)
* odoorpc (https://github.com/OCA/odoorpc)
* git-aggregator (https://github.com/acsone/git-aggregator)

Also this project is inspired by the following tools:

* click-odoo-contrib (https://github.com/acsone/click-odoo-contrib)


# Dockerfile information

### From version 5 to 7

There are no plans to make the tool work for these versions.

### From version 8 to 10 (Python2)

Try to create dockerfile, based on the odoo official ones fails. Any help welcome.

### From version 11.0 to latest version. (Python3)

The Dockerfile of the version 11 to the lastest version of Odoo are written this way :

- Copy the content of https://github.com/odoo/odoo/blob/ODOO_VERSION/setup/package.dfsrc
- remove all the part after the big ``apt-get install``
- install debian package ``git`` to have the possibility to pip install from git url.
- install custom debian packages
- install python odoo requirements
- install python ``setuptools-scm`` lib to have the possibility to pip install ``openupgradelib`` from git url.
- install python custom requirements
- makes link between external user and docker odoo user

## Réferences

- how to install gitlab runner locally:

https://docs.gitlab.com/runner/install/linux-manually.html

- Check your CI locally. (French)

https://blog.stephane-robert.info/post/gitlab-valider-ci-yml/

https://blog.callr.tech/building-docker-images-with-gitlab-ci-best-practices/


## Python version settings depending on the debian version

This part can help you if you want to change your autogenerated Dockerfiles.

See (https://github.com/odoo/odoo/blob/ODOO_VERSION/setup/package.dfdebian)

### debian:wheezy (V7) (for Odoo: 8.0)
- Ubuntu release : 12.04 xxx, 12.10 xxx, 13.04 xxx, 14.10 xxx
- python2.7
- First release : 04/05/2013
- End LTS : May 2018

### debian:jessie (V8) (for Odoo: 9.0, 10.0)
- Ubuntu release : 14.04 trusty, 14.10 utopic, 15.04 vivid, 15.10 wily
- python2.7
- First release : 26/04/2015
- End LTS : June 2020

### debian:stretch (V9) (for Odoo: 11.0, 12.0)
- Ubuntu releases : 16.04 xenial, 16.10 yakkety, 17.04 zesty, 17.10 artful
- python2.7 and python3.5
- First release : 17/06/2017
- End LTS : June 2022

### debian:buster (13.0, 14.0)
- Ubuntu release : 18.04 bionic, 18.10 cosmic, 19.04 disco, 19.10 eoan
- python2.7 and python3.7
- First release : 06/07/2019
- End LTS : Undefined.

## debian:bullseye (15.0, 16.0)
- Ubuntu release : 20.04 focal, 20.10 groovy, 21.04 hirsute, 21.10 impish
- python3.9
- First release : 14/07/2021
- End LTS : Undefined.

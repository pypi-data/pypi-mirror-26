Gestion des SAPMS
=================

Getting Started
---------------

- Change directory into your newly created project.

    cd ovhspams

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Run your project's tests.

    env/bin/pytest

- Download ini files

    wget http://static.frkb.fr/ovhspams/development.ini
    wget http://static.frkb.fr/ovhspams/production.ini

- Run your project.

    env/bin/pserve development.ini
    or
    env/bin/pserve production.ini

- Acces your project

  http://localhost:6543


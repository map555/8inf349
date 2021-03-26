# E-commerce app

Small E-commerce app made with Flask

## Project configuration
Make sure that these libraries are installed:
```
    OS:
        Ubuntu 20.04.2LTS
        Windows 10 64bits V20H2

    Python version:
        Python 3.8.5
        Python 3.9.1

    External libraries:
        Flask
            version: 1.1.2

        Peewee
            version: 3.14.1

        Pytest
            version: 6.2.2

        Schema
            version: 0.7.4



    IDE: Pycharm
        Edition: Professional
        version: 2020.3


    PyCharm project configuration type: Python

        note: We didn't use the PyCharm's Flask configuration because we couldn't configure the FLASK_APP parameter
        properly with this configuration. So we use a standard PyCharm's Python project configuration.

        Module name: flask
        Parameters: run

        Environment variable:
            PYTHONUNBUFFERED=1;FLASK_APP=Api8inf349;FLASK_ENV=development;FLASK_DEBUG=1

        Python interpreter:
            Python 3.8 (if python 3.8)
            Python 3.9 (if python 3.9)
```

## Usage

First we initialize the database with this command (in Api8inf349 directory):
```
$ FLASK_APP=Api8inf349 flask init-db
```

Then to run the server (in Api8inf349 directory):
```
$ FLASK_APP=__init__.py flask run
```

The app will now be available at http://localhost:5000/

## Tests

To run tests (in project root directory):

```
$ python -m pytest test/
```

To run tests and generate a html report (in project root directory):

```
HTML test coverage: python -m pytest --cov-report=html --cov=Api8inf349
```

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
            
        requests
            version: 2.25.1
            
        psycopg2
            version: 2.8.6
            
        rq
            version: 1.8.0
    
    *Docker and docker-compose need to be installed on the machine




    IDE: Pycharm
        Edition: Professional/Community
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

## Usage (Windows)

We start by launching the PostgreSQL database and the redis cache with docker compose:
```
$ docker-compose build
$ docker-compose up
```

Then we initialize the database with these commands:
```
$ set FLASK_DEBUG=True& set FLASK_APP=api8inf349& set REDIS_URL=redis://localhost& set DB_HOST=localhost& set DB_USER=user& set DB_PASSWORD=pass& set DB_PORT=5432& set DB_NAME=api8inf349
$ flask init-db
```

Then to run the server:
```
$ docker build -t api8inf349 .
$ docker run -p 5000:5000 -e REDIS_URL=redis://host.docker.internal -e DB_HOST=host.docker.internal -e DB_USER=user -e DB_PASSWORD=pass -e DB_PORT=5432 -e DB_NAME=api8inf349 api8inf349 
```

The app will now be available at http://localhost:5000/

## Usage (Linux)

We start by launching the PostgreSQL database and the redis cache with docker compose:
```
$ docker-compose build
$ docker-compose up
```

Then we initialize the database with these commands:
```
$ FLASK_DEBUG=True FLASK_APP=api8inf349 REDIS_URL=redis://localhost DB_HOST=localhost DB_USER=user DB_PASSWORD=pass DB_PORT=5432 DB_NAME=api8inf349
$ flask init-db
```

Then to run the server:
```
$ docker build -t api8inf349 .
$ docker run -p 5000:5000 -e REDIS_URL=redis://host.docker.internal -e DB_HOST=host.docker.internal -e DB_USER=user -e DB_PASSWORD=pass -e DB_PORT=5432 -e DB_NAME=api8inf349 api8inf349 
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

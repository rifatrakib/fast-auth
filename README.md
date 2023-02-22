# fastapi OAuth2.0

In this repository, a fully implemented *plug-and-play* style basic authentication system (OAuth2.0 complient) is implemented primarily with [fastapi](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/), [pydantic](https://docs.pydantic.dev/) along with some other modern Python libraries and packages, which can easily be extended for adding additional features on top. The logic handled here are transferable to any [fastapi](https://fastapi.tiangolo.com/) project, only except if someone plans to use any database that is not supported with [SQLAlchemy](https://www.sqlalchemy.org/) or a database driver for which [SQLAlchemy](https://www.sqlalchemy.org/) does not have a configuration.


## What you will find ...

* Fully useable authentication system using [fastapi](https://fastapi.tiangolo.com/) and any [SQLAlchemy](https://www.sqlalchemy.org/) supported relational database.
* All *table-mapping* [SQLAlchemy](https://www.sqlalchemy.org/) models required for authentication.
* System for authenticating users with JWT access tokens (with multiple configuration for expiries).
* *Asynchronous* implementation for database and path operations functions (**non-blocking I/O**).
* Asynchronous configuration of [alembic](https://alembic.sqlalchemy.org/en/latest/index.html) for managing database *versioning* and *migrations*.
* Most of the codes are *typed-checked*. Consistent schema definitions, automatic parsing and validation with [pydantic](https://docs.pydantic.dev/).
* Fully configured email service which can be used and extended as necessary.
* Multiple configuration settings which can be tried out only by changing one environment variable.
* Practical and easily understandable layout of modules. Separation of concerns and unit-tested.
* Codes are formatted with several [pre-commit](https://pre-commit.com/) hooks.
* Containerization using [Docker](https://docs.docker.com/) and local development support with [docker compose](https://docs.docker.com/compose/).


## How to install

This project has been containerized with necessary configurations for both productionizing and local development using [Docker](https://docs.docker.com/) and local development support with [docker compose](https://docs.docker.com/compose/) respectively.

First thing you need to do is to create a `.env` from the provided `.env.sample` file and fill in the fields as per your needs.

To use it on local environment, create your database and run:

```
virtualenv venv
pip install -r requirements.txt
poetry install
alembic upgrade head
```

and then run the docker compose using:

```
docker compose up
```

or you can follow these steps one by one to do it manually:

```
virtualenv venv
pip install -r requirements.txt
poetry install
alembic upgrade head
uvicorn server.main:app --reload
```

Access the routes for [OpenAPI documentation](http://127.0.0.1:8000/docs) or [ReDoc](http://127.0.0.1:8000/redoc) when the server is running.

Adding new things are very easy to do, follow these steps as a guideline (not mandatory):

1. Create database model in any script inside the `server/models` module, and make migrations by running `alembic revision --autogenerate -m "<some message>"`, followed by upgrading the database tables accordingly with `alembic upgrade head`.

2. Create necessary schemas using [pydantic](https://docs.pydantic.dev/) inside the `server/schemas` module (**name your scripts consistently for better organization**). It's best to inherit the classes in `server/schemas/base.py` for consistent configurations (`..API` for *path operation* related things, `..ORM` for *database side* of things).

3. Re-use the existing utility functions from `server/services` module or create new as needed.

4. Make a separate class for managing database queries to each table/models. This will keep the logics together and better for readability. See the modules inside `server/sql` for reference and put your classes inside this directory.

5. Make use of the dependencies and create your path operation functions following the pattern in `server/routers` module.

6. Add any new variable you need in the `server/core/environments` module, if the value is common for all modes, keep it in the `BaseConfig` of `server/core/environments/base.py` or else put the *mode-dependent* variables in their corresponding module/class.

7. Include your endpoints in the `server/main.py`, and you should be good to go!

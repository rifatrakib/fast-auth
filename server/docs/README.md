In this repository, a fully implemented plug-and-play style basic authentication system (OAuth2.0 complient) is implemented which can easily be extended for adding additional features on top. The logic handled here are transferable to any [fastapi](https://fastapi.tiangolo.com/) project, only except if someone plans to use any database that is not supported with [SQLAlchemy](https://www.sqlalchemy.org/) or a database driver for which [SQLAlchemy](https://www.sqlalchemy.org/) does not have a configuration.


## Features

* OAuth2.0 complience, follows OpenAPI conventions and has OpenAPI documentations.
* JWT access tokens (with multiple configuration for expiries).
* Multiple configuration settings which can be tried out only by changing one environment variable.
* Practical and easily understandable layout of modules.
* Separation of concerns and unit-tested.
* Consistent schema definitions, automatic parsing and validation.
* Asynchronous implementation for database and path operations (non-blocking I/O).
* Configured email service which can be used as necessary.
* Most of the objects are strongly typed.

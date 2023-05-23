# Django REST API

#### Django REST Framework integration with SQLAlchemy

The back-end API is responsible for handling file uploads, performing transformations on the data, and storing the data and transformation rules in a database. The API is built using Django and Django REST Framework, and uses SQL Alchemy and Pandas to perform the data transformations.

## Features

> Upload csv files.
> store the transformation rules.
> using pandas to handle transformation.
> Retrieve the CSV files and rules from the database as needed.

## Installation

requires Python3.x
Install the dependencies and start the server.

```zsh
cd etl_project_backend
python manage.py runserver
```

Dillinger is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8080, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image.

## License

MIT

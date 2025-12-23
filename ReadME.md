# Short link url

This project is a Python-based web service that allows users to shorten URLs, similar to TinyURL or bit.ly. It provides endpoints to create, update, and retrieve shortcodes for URLs.



### Prerequisites

- Docker and Docker Compose installed
- A `.env` file in the root directory. You can create it by copying the provided `dist.env` file or by running the command:

```bash
    cp dist.env .env
```



### Running the Project

To start the project, run the command:

```bash
    docker compose up --build
```
Once the containers are up, the application will be ready to use.

The configuration class `Settings` in `src/core/config.py` has an attribute `MIGRATION_ON_STARTUP` which is currently set to `True`. This ensures that database migrations are applied automatically at startup.



###  Accessing the API

You can access the API documentation and interact with the endpoints at:

**[http://localhost:8080/docs](http://localhost:8080/docs)**

Alternatively, you can use Postman or any HTTP client of your choice.



### Database Administration

PgAdmin has been added for convenient database inspection and management:

**[http://localhost:5050/browser/](http://localhost:5050/browser/)**

To log in and connect to the database, use the credentials defined in the `.env` file.


### Running Tests

First, enter the application container using the following command:

```bash
    docker compose exec api /bin/bash
```

Then, run the tests with command:

```
  pytest
```



### Pre-commit Hooks

The project includes a `.pre-commit-config.yaml` file, which automatically runs code checks and the linter before each commit.



# Potential Improvements

- Add `redis` as a caching layer for frequently accessed short URLs to significantly speed up redirects and reduce database load.
- Add more validation for `shortcodes` to ensure they meet certain standards.
- Add centralized, structured `logging` to improve observability, simplify debugging, and support effective monitoring in production environments.
- The update endpoint was initially documented as a `POST` method. It has been changed to `PATCH` to comply with RESTful principles.
- Implement integration tests to cover the full workflow of the service, not just unit tests.

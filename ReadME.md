# Short link url

This project is a Python-based web service that allows users to shorten URLs, similar to TinyURL or bit.ly. It provides endpoints to create, update, and retrieve shortcodes for URLs.



### Prerequisites

- Docker and Docker Compose installed
- A `.env` file in the root directory, you can create it by copying the provided `dist.env` or run the command:

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



### Running Tests

To run unit tests:

```bash
    poetry run pytest
```



###  Pre-commit Hooks

To activate and use the pre-commit hooks:

```bash
    pre-commit install
```



# Potential Improvements

- Add more validation for `shortcodes` to ensure they meet certain standards.
- The update endpoint was initially documented as a `POST` method. It has been changed to `PATCH` to comply with RESTful principles.
- Implement integration tests to cover the full workflow of the service, not just unit tests.

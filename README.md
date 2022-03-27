Flask Application Quick Start Template
======================================

This repo provides a quick-start template for creating a stand-alone web application using the [Flask](http://flask.pocoo.org/) micro-framework for Python 3.8+. You can use this template as a basis for an app that will serve HTML and other content or as a starting point for an API-only service that will be paired with an SPA (React, Angular, etc.) or some other type of client.

Features:
* Flask 2.x and blueprints
* Jinja2 HTML templates
* SQLAlchemy database models
* Marshmallow for object marshalling
* JSON Web Token (JWT) authentication
* PyTest unit-tests
* Serve in production with waitress
* Pylint and Black

See [RESTful Flask application quick-start](http://keathmilligan.net/restful-flask-application-quick-start/) for more info.

## Getting Started

You will need Python 3.8 or later. Use the appropriate installation method for your system to install Python and make sure it is in your path. The template currently targets Python 3.10 (recommended).

This project also uses [pipenv](https://pipenv.pypa.io/en/latest/) to manage dependencies and its virtual environment. You will need to install it if you do not already have it.

### Using the template

To use the template, click the **Use this template** button in the [Github repository](https://github.com/keathmilligan/flask-quickstart) to create a new project using this code as a basis. Alternatively, you can clone the repository locally.

### Install dependencies

> The template currently expects Python 3.10, if you need to use an older version, you will need to modify the `Pipfile`.

Use [pipenv](https://pipenv.pypa.io/en/latest/) to create a virtual environment and install the dependencies:

```
pipenv install --dev
```

The `--dev` option will also install the optional development dependencies such as `pylint` and `pytest`.

## Running

### Create the database

Before running the app for the first time, you must initialize the database with:

Linux/MacOS:
```bash
export FLASK_APP=sample; pipenv run flask initdb
```

Windows Powershell
```powershell
$env:FLASK_APP = "sample"; pipenv run flask initdb
```

### Running in Development

To start the development server with automatic reloading, run:

Linux/MacOS:
```bash
export FLASK_APP=sample; pipenv run flask run --debugger --reload --with-threads
```

Windows Powershell
```powershell
$env:FLASK_APP = "sample"; pipenv run flask run --debugger --reload --with-threads
```

The app will be available with `http://localhost:5000`. Log in with the test user name `user1` and password `1234`:
![screenshot](/docs/images/screenshot.png)

Click the **Contacts** link to list and create sample data.

![contacts](/docs/images/contacts.png)

Edit a contact:

![edit contact](/docs/images/edit-contact.png)

### Running in Production

To serve the app with `waitress` for production use, run:

```
pipenv run python -m sample
```

Hit `Ctrl-C` to abort.

This is just a starting point for production deployment - see the [waitress docs](https://docs.pylonsproject.org/projects/waitress/en/latest/usage.html) for more info.

## Test

Run the `pytest` unit tests with:

```
pipenv run pytest
```

You should see something like:
```
======================================================= test session starts ========================================================
platform darwin -- Python 3.5.2, pytest-3.0.3, py-1.4.31, pluggy-0.4.0
rootdir: /Users/kmilligan/workspace/flask-quickstart, inifile: 
collected 11 items 

tests/test_auth.py ......
tests/test_contacts.py .....

==================================================== 11 passed in 2.90 seconds =====================================================
```

## REST API Usage

Use an HTTP client such as [PostMan](https://www.postman.com/) or the VSCode [Thunder Client](https://marketplace.visualstudio.com/items?itemName=rangav.vscode-thunder-client) extension to experiment with the REST API endpoints:

### Authenticate

Before you can access secured endpoints, you must obtain a JWT access token. Send a POST request to `http://127.0.0.1:5000/api/login` with the username/password to login and get an access token and a refresh token:

![Authenticate](/docs/images/rest-login.png)

Copy the access token to the clipboard - you will need it for subsequent requests. Also, save the refresh token somewhere, we'll use it later.

To verify that you have a valid access token, create a new GET request to `http://127.0.0.1:5000/api/auth` and set the "Authorization" type to "Bearer Token" and paste the access token into the Token field and send the request (alternatively, set the `Authorization` header to "Bearer `<access token>`").

![Verify Authentication](/docs/images/rest-get-auth.png)

### Refresh Access Token

If the access token has expired or is about to expire, you can obtain a new one by using the `api/refresh` endpoint:

![Refresh Access Token](/docs/images/rest-refresh.png)

### Use Sample Data Endpoints

Now you can use the sample contacts endpoints to list, create, update and delete entries:

![Get Contacts](/docs/images/rest-contacts.png)

## Next Steps

### Delete the stuff you don't need

For example, if you don't need to serve HTML, you can remove the `templates` directory and the page-oriented views from the blueprints. Alternatively, if you don't need to serve RESTful resources, you can delete the API endpoints.

### Add a real authentication backend

A real application will likely use some external service to lookup users, validate passwords, control access, etc. Enhance the `auth.py` module with your own authentication/authorization logic.

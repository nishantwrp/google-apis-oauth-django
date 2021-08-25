# Google APIs OAuth Django

[![PyPI version](https://badge.fury.io/py/google-apis-oauth-django.svg)](https://badge.fury.io/py/google-apis-oauth-django) [![Downloads](https://pepy.tech/badge/google-apis-oauth-django)](https://pepy.tech/project/google-apis-oauth-django)

A library to help integrate Google OAuth 2.0 to your Django application. This library retrieves the necessary tokens you need to access the Google APIs your application is configured for.

## Installation
```bash
pip install google-apis-oauth-django
```

## Usage

### Redirecting users to the login screen

```python
from django.shortcuts import HttpResponseRedirect
import google_apis_oauth

def RedirectToOAuthPage(request):
    oauth_url = google_apis_oauth.get_authorization_url(
        # Path of the "client_id.json" file
        JSON_FILEPATH,
        # Authorization scopes required
        SCOPES,
        # The url where the google oauth should redirect
        # after a successful login.
        REDIRECT_URI,
        # Force the consent prompt even if the user was authorized
        # previously. Defaults to False.
        True)
    return HttpResponseRedirect(url)
```

### Retreving and storing the credentials after successful login

```python
import google_apis_oauth

def RedirectView(request):
    try:
        # Get user credentials
        credentials = google_apis_oauth.get_crendentials_from_callback(
            request,
            JSON_FILEPATH,
            SCOPES,
            REDIRECT_URI
        )

        # Stringify credentials for storing them in the DB
        stringified_token = google_apis_oauth.stringify_credentials(
            credentials)

        # Store the credentials safely in the DB
        ...

        # Now that you have stored the user credentials you
        # can redirect user to your main application.
        ...
    except google_apis_oauth.exceptions.InvalidLoginException:
        # Handle unauthenticated request to the callback uri.
```

### Loading and using the user credentials
```python
import google_apis_oauth
from googleapiclient.discovery import build

# Use the stringified token to get a credentials object
# that can be used to authenticate requests made by
# google-api-python-client
# refreshed is a boolean that tells if the token was expired and was renewed.
# You may want to update the credentials in the database if it is True.
creds, refreshed = google_apis_oauth.load_credentials(stringified_token)

# Using credentials in google-api-python-client.
service = build('calendar', 'v3', credentials=creds)
...
```

## Example
You can refer to [this](https://www.nishantwrp.com/posts/google-apis-oauth-in-django/) blog for an example where this library is used.

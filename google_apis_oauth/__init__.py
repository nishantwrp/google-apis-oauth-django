"""Google APIs OAuth Django."""

import datetime
import json
import google.auth
import google.oauth2
import google_auth_oauthlib.flow

from .exceptions import InvalidLoginException

def get_authorization_url(client_json_filepath, scopes, redirect_uri, consent_prompt=False):
    """Get an authorization url for initiating google oauth.

    Args:
        client_json_filepath (str): Path where your client_id.json file is located.
        scopes (list(str)): Authorization scopes required.
        redirect_uri (str): The url where the google oauth should redirect after a successful login.
        consent_prompt (bool, optional): Force the consent prompt even if the user was authorized
            previously. Defaults to False.

    Returns:
        str: Authorization url where you should redirect user for google oauth.
    """
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_json_filepath,
        scopes=scopes
    )
    flow.redirect_uri = redirect_uri

    if consent_prompt:
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scope='true',
            prompt='consent'
        )
    else:
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scope='true'
        )

    return authorization_url

def get_crendentials_from_callback(request, client_json_filepath, scopes, redirect_uri):
    """Get credentials object from the callback request after a successful login.

    Args:
        request (Request): The django view request argument.
        client_json_filepath (str): Path where your client_id.json file is located.
        scopes (list(str)): Authorization scopes required.
        redirect_uri (str): The url where the google oauth should redirect after a successful login.

    Raises:
        InvalidLoginException: If an unauthenticated request is made to the redirect uri.

    Returns:
        Credentials: The credentials object which can be used to authenticate google APIs.
    """
    state = request.GET.get('state', None)

    if not state:
        raise InvalidLoginException

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_json_filepath,
        scopes=scopes,
        state=state
    )
    flow.redirect_uri = redirect_uri

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    return credentials

def stringify_credentials(credentials):
    """Convert the credentials object to a string. So that it can be stored easily.

    Args:
        credentials (Credentials): The credentials object.

    Returns:
        str: Stringified credentials which can be stored.
    """
    credentials_dict = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'id_token':credentials.id_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
        'expiry':datetime.datetime.strftime(credentials.expiry, '%Y-%m-%d %H:%M:%S')
    }
    return json.dumps(credentials_dict)

def load_credentials(stringified_credentials):
    """Load the credentials from the stringified version. Refreshes the access token if required.

    Args:
        stringified_credentials (str): Stringified credentials.

    Returns:
        Credentials: The credentials object which can be used to authenticate google APIs.
    """
    credentials_dict = json.loads(stringified_credentials)
    credentials = google.oauth2.credentials.Credentials(
        credentials_dict['token'],
        refresh_token=credentials_dict['refresh_token'],
        id_token=credentials_dict['id_token'],
        token_uri=credentials_dict['token_uri'],
        client_id=credentials_dict['client_id'],
        client_secret=credentials_dict['client_secret'],
        scopes=credentials_dict['scopes'],
    )

    expiry = datetime.datetime.strptime(credentials_dict['expiry'], '%Y-%m-%d %H:%M:%S')
    credentials.expiry = expiry

    request = google.auth.transport.requests.Request()
    refreshed = False
    if credentials.expired:
        credentials.refresh(request)
        refreshed = True

    return credentials, refreshed

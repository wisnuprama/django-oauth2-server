import base64
from rest_framework.response import Response

from apps.credentials.models import OAuthClient


def client_credentials_required(view):
    def wrapper(request, *args, **kwargs):
        client = _check_client_credentials_in_header(request=request)
        if not client:
            client = _check_client_credentials_in_post(request=request)

        if not client:
            response = Response(data={
                'error': u'invalid_client',
                'error_description': u'Client credentials were not found in the headers or body',
            }, status=401)
            response['WWW-Authenticate'] = 'Basic realm="django-oauth2-server"'
            return response

        request.client = client
        return view(request, *args, **kwargs)
    return wrapper


def grant_type_required(view):
    def wrapper(request, *args, **kwargs):
        if 'grant_type' not in request.POST:
            response = Response(data={
                'error': u'invalid_request',
                'error_description': u'The grant type was not specified in the request',
            }, status=400)
            return response

        request.grant_type = request.POST['grant_type']
        return view(request, *args, **kwargs)
    return wrapper


def _check_client_credentials_in_header(request):
    if not 'HTTP_AUTHORIZATION' in request.META:
        return False

    auth_method, auth = request.META['HTTP_AUTHORIZATION'].split(': ')
    if auth_method.lower() != 'basic':
        return False

    client_id, client_secret = base64.b64decode(auth).split(':')
    try:
        client = OAuthClient.objects.get(client_id=client_id)
    except OAuthClient.DoesNotExist:
        return False

    if not client.verify_password(client_secret):
        return False

    return client


def _check_client_credentials_in_post(request):
    if 'client_id' not in request.POST:
        return False

    if 'client_secret' not in request.POST:
        return False

    client_id = request.POST.get('client_id')
    client_secret = request.POST.get('client_secret')
    client = OAuthClient.objects.get(client_id=client_id)

    if not client.verify_password(client_secret):
        return False

    return client
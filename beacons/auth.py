from django.http.response import JsonResponse
from beacons.models import Token

from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.handlers.base import logger
import hashlib
from beacons.thread_local import get_current_request


def token_required(func):
    def inner(cl, request, *args, **kwargs):
        if request.method == 'OPTIONS':
            return func(cl, request, *args, **kwargs)

        if request.user.is_authenticated():
            return func(cl, request, *args, **kwargs)

        token = request.META.get('HTTP_AUTH_TOKEN')
        if not token:
            logger.debug('Missing Auth-Token header')
            return JsonResponse({'error': 'Missing Auth-Token header'}, status=403)

        user = authenticate(token=token)
        if not user or not user.is_authenticated():
            logger.debug('User not found')
            return JsonResponse({'error': 'User not found'}, status=403)

        request.user = user
        request.token = Token.objects.get(token=token)

        return func(cl, request, *args, **kwargs)

    return inner


def weblogin_required(func):
    def inner(cl, request, *args, **kwargs):
        if request.method == 'OPTIONS':
            return func(cl, request, *args, **kwargs)

        if request.user.is_authenticated():
            return func(cl, request, *args, **kwargs)

        return JsonResponse({'error': 'You are not logged in'}, status=403)

    return inner


class TokenBackend(ModelBackend):
    def authenticate(self, token):
        clear_expired_tokens()

        try:
            token = Token.objects.get(token=token)
        except Token.DoesNotExist:
            return None

        user = token.user
        if not user:
            return None

        token.update_expiration()
        token.last_active_at = timezone.now()
        token.save()
        return user

#
# class UserBackend(ModelBackend):
#     def authenticate(self, username, password):
#         request = get_current_request()
#
#         uri = request.get_full_path()
#         # generate md5 from password when request is ajax or for admin login
#         if request.is_ajax() or uri.startswith('/admin'):
#             password = hashlib.md5(password).hexdigest()
#
#         return ModelBackend.authenticate(self, username, password)

def clear_expired_tokens():
    Token.objects.filter(expire_at__lt=timezone.now()).delete()
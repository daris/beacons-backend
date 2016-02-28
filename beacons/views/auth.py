# coding=utf-8
import json

from beacons.auth import token_required
from beacons.models import Beacon, Store, User, StoreOffer, Token
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from push_notifications.models import GCMDevice


class SetPushTokenView(View):

    def post(self, request):
        data = json.loads(request.body)
        token = data.get('token')

        user = User.objects.get(id=1)

        GCMDevice.objects.filter(user=user).delete()
        GCMDevice.objects.create(user=user, registration_id=token)

        return JsonResponse({'success': 'ok'}, safe=False)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)


class LoginView(View):

    def post(self, request):
        data = json.loads(request.body)

        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is None:
            # the authentication system was unable to verify the username and password
            return JsonResponse({'error': "Nazwa użytkownika lub hasło jest nieprawidłowa"}, status=401)

        if not user.is_active:
            return JsonResponse({'error': "Konto zostało zdezaktywowane"}, status=401)

        request.user = user

        token = create_user_token(user)

        result = {
            'token': token.token,
            'user': user.as_json(),
        }

        login(request, user)

        return JsonResponse(result, safe=False)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request)


class LogoutView(View):
    def post(self, request):
        data = json.loads(request.body)

        user = request.user
        user.tokens.delete()
        GCMDevice.objects.filter(user=user).delete()

        logout(request)

        return JsonResponse({'success': 'ok'})

    @csrf_exempt
    @token_required
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request)


def create_user_token(user):
    token = Token()
    token.user = user
    token.created_at = timezone.now()
    token.update_expiration()
    token.save()

    return token

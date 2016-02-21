import json

from beacons.models import Beacon, Store, User, StoreOffer
from django.db.models import Q
from django.http import JsonResponse
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


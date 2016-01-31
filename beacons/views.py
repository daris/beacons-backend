import json

from beacons.models import Beacon, Store
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from push_notifications.models import GCMDevice


class BeaconsListView(View):

    def get(self, request):
        uuids = Beacon.objects.values_list('uuid', flat=True).distinct()
        
        result = {
            'beacons': [{'uuid': u} for u in uuids]
        }
        return JsonResponse(result, safe=False)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)


class BeaconsSeenView(View):

    def post(self, request):
        data = json.loads(request.body)
        beacons_data = data.get('beacons', [])

        filters = Q()
        for beacon_data in beacons_data:
            filters |= Q(uuid=beacon_data.get('uuid'), major=beacon_data.get('major'), minor=beacon_data.get('minor'))

        beacons = Beacon.objects.filter(filters)
        for beacon in beacons:
            if not beacon.shop:
                continue

            device = GCMDevice.objects.get(user__id=1)
            device.send_message("New promotions for %s!" % beacon.shop.name)

        result = {
            'b': [b.as_json() for b in beacons]
        }
        return JsonResponse(result, safe=False)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)


class StoresListView(View):

    def get(self, request):
        stores = Store.objects.all()

        result = {
            'stores': [s.as_json() for s in stores]
        }
        return JsonResponse(result, safe=False)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
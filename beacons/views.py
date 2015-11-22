from beacons.models import Beacon, Store
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


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
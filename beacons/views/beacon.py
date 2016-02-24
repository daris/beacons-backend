import json

from beacons.models import Beacon, Store, User, StoreOffer
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

        user = User.objects.get(id=1)

        filters = Q()
        for beacon_data in beacons_data:
            filters |= Q(uuid=beacon_data.get('uuid'), major=beacon_data.get('major'), minor=beacon_data.get('minor'))

        beacons = Beacon.objects.filter(filters)
        store_ids = [b.store_id for b in beacons if b.store]
        if not store_ids:
            return JsonResponse({'message': 'No stores matched for given beacons.'}, safe=False)

        stores = Store.objects.filter(id__in=store_ids)
        for store in stores:
            offers = store.offers.all()
            for offer in offers:
                if user.has_seen_offer(offer):
                    continue

                device = GCMDevice.objects.get(user=user)
                device.send_message("%s: %s!" % (store.name, offer.name), extra={"offerId": offer.id})

                user.mark_offer_as_seen(offer)

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


class StoreOfferView(View):

    def get(self, request, offer_id):
        try:
            offer = StoreOffer.objects.get(id=offer_id)
        except StoreOffer.DoesNotExist:
            return JsonResponse({'error': 'Offer was not found'})

        result = {
            'offer': offer.as_json()
        }
        return JsonResponse(result, safe=False)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)


class StoreOffersView(View):

    def get(self, request, store_id):
        offers = StoreOffer.objects.filter(store__id=store_id).all()

        result = {
            'offers': [s.as_json() for s in offers]
        }
        return JsonResponse(result, safe=False)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

from beacons.models import Store, Beacon, User, StoreOffer
from django.contrib import admin


class StoreAdmin(admin.ModelAdmin):
    pass


class StoreOfferAdmin(admin.ModelAdmin):
    pass


class BeaconAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Store, StoreAdmin)
admin.site.register(StoreOffer, StoreOfferAdmin)
admin.site.register(Beacon, BeaconAdmin)
admin.site.register(User, UserAdmin)

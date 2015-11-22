from beacons.models import Store, Beacon
from django.contrib import admin


class StoreAdmin(admin.ModelAdmin):
    pass


class BeaconAdmin(admin.ModelAdmin):
    pass


admin.site.register(Store, StoreAdmin)
admin.site.register(Beacon, BeaconAdmin)

from beacons.models import Store, Beacon, User, StoreOffer, SeenOffer
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django import forms


class SeenOfferAdmin(admin.ModelAdmin):
    list_display = ('offer', 'user')


class MyUserChangeForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)


class UserAdmin(admin.ModelAdmin):
    form = MyUserChangeForm

    def save_model(self, request, obj, form, change):

        # Override this to set the password to the value in the field if it's
        # changed.
        if obj.pk:
            password = request.POST.get('password', None)
            if password:
                obj.set_password(password)
        obj.save()


admin.site.register(Store)
admin.site.register(StoreOffer)
admin.site.register(Beacon)
admin.site.register(User, UserAdmin)
admin.site.register(SeenOffer, SeenOfferAdmin)

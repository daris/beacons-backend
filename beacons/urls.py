"""beacons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from beacons import settings
from beacons.views.auth import SetPushTokenView
from beacons.views.beacon import BeaconsListView, StoresListView, BeaconsSeenView, StoreOfferView
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    url(r'^api/set_push_token', SetPushTokenView.as_view(), name="api_set_push_token"),

    url(r'^api/beacons_seen', BeaconsSeenView.as_view(), name="api_beacons"),
    url(r'^api/beacons', BeaconsListView.as_view(), name="api_beacons"),

    url(r'^api/offers/(?P<offer_id>\d+)', StoreOfferView.as_view(), name="api_store_offer"),

    url(r'^api/stores', StoresListView.as_view(), name="api_stores"),

    url(r'^admin/', include(admin.site.urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

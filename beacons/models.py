# coding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class PortalUserManager(BaseUserManager):
    pass


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    objects=PortalUserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin


class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Beacon(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    uuid = models.CharField(max_length=50, blank=True, null=True)
    minor = models.IntegerField(blank=True, null=True)
    major = models.IntegerField(blank=True, null=True)
    store = models.ForeignKey(Store, db_column='store_id', related_name='beacons', blank=True, null=True)


class StoreOffer(models.Model):
    image = models.ImageField(upload_to="store_offers", blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    store = models.ForeignKey('Store', db_column="store_id", related_name='offers', blank=True, null=True)

    def as_json(self):
        return dict(
            promotionId=self.id,
            promotionName=self.name,
            imageUrl=media_url(self.image.name) if self.image else '',
            storeId=self.store.id if self.store else None,
            storeName=self.store.name if self.store else None,
        )

    def __unicode__(self):
        return '%d, %s' % (self.id, self.name)


class SeenOffer(models.Model):
    offer = models.ForeignKey(StoreOffer, related_name='seen_offers')
    user = models.ForeignKey(User, related_name='seen_offers')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s, %s' % (self.offer, self.user)
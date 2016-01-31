# coding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from beacons.utils import media_url
from django.utils import timezone


class PortalUserManager(BaseUserManager):
    def _create_user(self, username, password, is_admin, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, last_login=now, is_admin=is_admin, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, **extra_fields)



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

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_seen_offer(self, offer):
        return self.seen_offers.filter(offer=offer, user=self).count() > 0

    def mark_offer_as_seen(self, offer):
        self.seen_offers.create(offer=offer)


class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def as_json(self):
        return dict(
            id=self.id,
            name=self.name,
            description=self.description,
        )

    def __unicode__(self):
        return self.name


class Beacon(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    uuid = models.CharField(max_length=50, blank=True, null=True)
    minor = models.IntegerField(blank=True, null=True)
    major = models.IntegerField(blank=True, null=True)
    store = models.ForeignKey(Store, db_column='store_id', related_name='beacons', blank=True, null=True)

    def as_json(self):
        return dict(
            id=self.id,
            name=self.name,
            uuid=self.uuid,
            minor=self.minor,
            major=self.major,
            store=self.store.name,
        )



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

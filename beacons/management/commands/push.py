from django.core.management.base import BaseCommand, CommandError
from push_notifications.models import GCMDevice


class Command(BaseCommand):
    help = 'Sends push message'

    def handle(self, *args, **options):
        device = GCMDevice.objects.get(user_id=1)
        # The first argument will be sent as "message" to the intent extras Bundle
        # Retrieve it with intent.getExtras().getString("message")
        device.send_message("New promotions!")
        # If you want to customize, send an extra dict and a None message.
        # the extras dict will be mapped into the intent extras Bundle.
        # For dicts where all values are keys this will be sent as url parameters,
        # but for more complex nested collections the extras dict will be sent via
        # the bulk message api.
        device.send_message(None, extra={"offerId": 1})

        self.stdout.write('Done')
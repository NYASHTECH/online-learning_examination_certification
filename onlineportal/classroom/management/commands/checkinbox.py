from django.core.management.base import BaseCommand, CommandError
import django
from django.conf import settings
from django.core.mail import send_mail
from classroom.models import LandpageContactMessage

class Command(BaseCommand):
    help = 'Checks inboxes and sends all the emails to the specified address emails'
    
    def handle(self, *args, **options):
        """
            Function iterates through all the messages left for us on the 
            landpage and emails these messages to the contact lists.
        """
        contact_list = ["nyashajah@gmail.com", "nshanganye@gmail.com", "tc@hit.co.zw"]
        
        try:
           messages = LandpageContactMessage.objects.all()
        except LandpageContactMessage.DoesNotExist:
           return

        # Send our messages and then delete them from the database.
        for message in messages:
            """
               Please note, since we are using gmail, we need "Access for
               less secure apps" to be "Turned On".
            """
            text = "FROM: " + message.email + "\n"
            text += "NAME: " + message.name + "\n"
            text += "PHONE: " + message.phone + "\n"
            text += "MESSAGE: " + message.message + "\n"
            
            send_mail(
                "Landpage Message",
                text,
                settings.EMAIL_HOST_USER,
                contact_list,
                fail_silently=False)

            message.delete() # Delete our message


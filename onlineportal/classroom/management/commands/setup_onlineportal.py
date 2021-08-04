from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from classroom.models import LandpageTeamMember
from classroom.models import LandpagePartner

class Command(BaseCommand):
    """
        Run in your console:
        $ python manage.py setup_academicstoday
    """
    help = 'Picks the top 9 courses with the highest student enrollment.'
    
    def handle(self, *args, **options):
        """
            Function will create the objects necessary for some of the UI
            elements in the landpage.
        """
        LandpageTeamMember.objects.all().delete()
        LandpageTeamMember.objects.create(
            id=1,
            full_name="Nyasha Shanganye",
            role="Lead Developer",
            twitter_url="https://twitter.com/NyashaShangaye",
            facebook_url="https://www.facebook.com/NyashaShanganye",
            image_filename="nyasha.png",
            linkedin_url="https://www.linkedin.com/pub/nyashashanganye",
            email="nshanganye@gmail.com",
        )
        LandpageTeamMember.objects.create(
            id=2,
            full_name="Taurai Chiwawa",
            role="Lead Designer",
            twitter_url="https://twitter.com/tauraichiwawa",
            facebook_url="https://www.facebook.com/tauraichiwawa",
            image_filename="chiwawa.png",
            github_url="https://github.com/tauraichiwawa",
            email="tauraichiwawa@gmail.com",
        )
        LandpageTeamMember.objects.create(
            id=3,
            full_name="Kudakwashe Maramba",
            role="Developer",
            twitter_url="https://twitter.com/kudakwashemaramba",
            google_url="https://plus.google.com/u/0/108001172254765225648/posts",
            image_filename="kudakwashe.png",
            linkedin_url="http://ca.linkedin.com/pub/kudakwashemaramba",
            email="kudakwashemaramba@gmail.com",
        )

        LandpagePartner.objects.all().delete()
        LandpagePartner.objects.create(
            id=1,
            image_filename="duplexsoft.png",
            title="Duplexsoft",
            url="www.duplexsoft.com"
        )
        LandpagePartner.objects.create(
            id=2,
            image_filename="eurasiasoft.png",
            title="Eurasiasoft",
            url="www.eurasiasoft.com"
        )

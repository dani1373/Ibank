from django.core.management.base import BaseCommand

from modir.models import BankAdmin
from profile.models import Profile


class Command(BaseCommand):
    help = 'Create bank admin'

    def handle(self, *args, **options):
        data = {
            'first_name': 'Modir',
            'last_name': 'Ibank',
            'national_id': '1234567890',
            'phone_number': '09123456789',
            'address': 'Iran - Tehran - Ibank',
        }

        BankAdmin.objects.all().delete()
        if Profile.objects.filter(national_id=data['national_id']).exists():
            profile = Profile.objects.get(national_id=data['national_id'])
            profile.user.delete()
            profile.delete()

        profile = Profile.register(data=data)
        profile.user.set_password('123456')
        profile.user.save()
        profile.password = '123456'
        profile.save()

        BankAdmin.objects.create(profile=profile)

        print 'Bank admin %s %s created successfully with username %s and password %s' \
              % (profile.user.first_name, profile.user.last_name, profile.national_id, profile.password)

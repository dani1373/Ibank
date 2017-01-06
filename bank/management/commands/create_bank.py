from django.core.management.base import BaseCommand

from bank.models import Bank
from modir.models import BankAdmin


class Command(BaseCommand):
    help = 'Create bank'

    def handle(self, *args, **options):
        Bank.objects.all().delete()

        bank_admin = BankAdmin.objects.all()[0]
        Bank.objects.create(admin=bank_admin)

        print 'bank created with administration of %s %s' % (bank_admin.profile.user.first_name,
                                                             bank_admin.profile.user.last_name)

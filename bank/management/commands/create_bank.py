from django.core.management.base import BaseCommand

from atm.models import Money
from bank.models import Bank
from customer.models import Account
from modir.models import BankAdmin


class Command(BaseCommand):
    help = 'Create bank'

    def handle(self, *args, **options):
        Bank.objects.all().delete()

        bank_admin = BankAdmin.objects.all()[0]
        Bank.objects.create(admin=bank_admin)
        Account.objects.create(account_number=1)
        moneys = ['1000', '2000', '5000', '10000', '50000', '100000']
        for amount in moneys:
            Money.objects.create(amount=amount)

        print 'bank created with administration of %s %s' % (bank_admin.profile.user.first_name,
                                                             bank_admin.profile.user.last_name)

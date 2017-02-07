from __future__ import unicode_literals

from django.db import models

from atm.models import ATM
from customer.models import Account
from service.models import Cheque, PeriodicOrder, Bill


class Transaction(models.Model):
    TYPE_CHOICES = (
        ('T', 'Transfer'),
        ('W', 'Withdraw'),
        ('D', 'Deposit'),
    )

    METHOD_CHOICES = (
        ('C', 'Cheque'),
        ('A', 'ATM'),
        ('P', 'Periodic'),
        ('B', 'Bill'),
        ('H', 'Physical'),
    )

    source_account = models.ForeignKey(Account, null=True, related_name='source')
    destination_account = models.ForeignKey(Account, null=True, related_name='destination')

    cheque = models.ForeignKey(Cheque, null=True)
    atm = models.ForeignKey(ATM, null=True)
    periodic_order = models.ForeignKey(PeriodicOrder, null=True)
    bill = models.ForeignKey(Bill, null=True)

    amount = models.PositiveIntegerField()

    type = models.CharField(max_length=1, choices=TYPE_CHOICES, db_index=True, null=False, blank=False)
    method = models.CharField(max_length=1, choices=METHOD_CHOICES, db_index=True, null=False, blank=False)

    create_time = models.DateTimeField(auto_now_add=True)

from __future__ import unicode_literals

from django.db import models

from bank.models import Branch
from customer.models import Account
from employee.models import Employee


class ATM(models.Model):
    branch = models.ForeignKey(Branch)


# just for stats
class AddMoney(models.Model):
    atm = models.ForeignKey(ATM)

    employee = models.ForeignKey(Employee)

    amount = models.PositiveIntegerField(unique=True, null=False, blank=False, db_index=True)
    count = models.PositiveIntegerField(default=0, null=False, blank=False, db_index=True)


class Money(models.Model):
    atm = models.ForeignKey(ATM)

    amount = models.PositiveIntegerField(unique=True, null=False, blank=False, db_index=True)
    count = models.PositiveIntegerField(default=0, null=False, blank=False, db_index=True)
    minimum_to_notify = models.PositiveIntegerField(default=0, null=False, blank=False, db_index=True)


class Card(models.Model):
    account = models.ForeignKey(Account)

    pin = models.CharField(max_length=4, null=False, blank=False, default='0000')
    card_number = models.CharField(max_length=16, null=False, blank=False, unique=True, db_index=True)

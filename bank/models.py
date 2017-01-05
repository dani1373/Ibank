from __future__ import unicode_literals

from django.db import models

from modir.models import BankAdmin, BranchAdmin
from profile.models import Profile


class Bank(models.Model):
    admin = models.ForeignKey(BankAdmin)

    annual_profit = models.FloatField(default=0)

    card_commission = models.PositiveIntegerField(default=0)
    cheque_commission = models.PositiveIntegerField(default=0)
    sms_commission = models.PositiveIntegerField(default=0)
    card_to_card_commission = models.PositiveIntegerField(default=0)
    transfer_commission = models.PositiveIntegerField(default=0)


class Branch(models.Model):
    admin = models.ForeignKey(BranchAdmin)

    address = models.CharField(max_length=100, null=False, blank=False)

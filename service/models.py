from __future__ import unicode_literals

from django.db import models

from customer.models import Account


class ChequeBook(models.Model):
    # TODO one user one cheque
    account = models.ForeignKey(Account)


class Cheque(models.Model):
    STATE_CHOICES = (
        ('N', 'Not Used'),
        ('WL', 'Waiting for Lawyer'),
        ('WA', 'Waiting for Auditor'),
        ('V', 'Verified'),
        ('DL', 'Declined by Lawyer'),
        ('DA', 'Declined by Auditor'),
    )

    cheque_book = models.ForeignKey(ChequeBook)

    amount = models.PositiveIntegerField(default=0, null=False, blank=False, db_index=True)

    state = models.CharField(max_length=2, choices=STATE_CHOICES, default='N', db_index=True)


class BillType(models.Model):
    destination_account = models.ForeignKey(Account)

    name = models.CharField(max_length=100, null=False, blank=False, db_index=True)


class Bill(models.Model):
    bill_type = models.ForeignKey(BillType)

    amount = models.PositiveIntegerField(null=False, blank=False, db_index=True)
    payer = models.CharField(max_length=10, null=False, blank=False, db_index=True)  # national id of payer


class Loan(models.Model):
    STATE_CHOICES = (
        ('WL', 'Waiting for Lawyer'),
        ('WA', 'Waiting for Auditor'),
        ('V', 'Verified'),
        ('DL', 'Declined by Lawyer'),
        ('DA', 'Declined by Auditor'),
        ('D', 'Done'),
    )

    account = models.ForeignKey(Account)

    amount = models.PositiveIntegerField(null=False, blank=False, db_index=True)
    count = models.PositiveIntegerField(null=False, blank=False, db_index=True)

    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='WL', db_index=True)


class PeriodicOrder(models.Model):
    TYPE_CHOICES = (
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Y', 'Yearly'),
    )

    STATE_CHOICES = (
        ('I', 'In Progress'),
        ('D', 'Done'),
    )

    loan = models.ForeignKey(Loan)

    start_time = models.DateField(null=False, blank=False, db_index=True)
    count = models.PositiveIntegerField(null=False, blank=False, db_index=True)
    amount = models.PositiveIntegerField(null=False, blank=False, db_index=True)

    state = models.CharField(max_length=1, default='I', choices=STATE_CHOICES, db_index=True)
    type = models.CharField(max_length=1, default='D', choices=TYPE_CHOICES, db_index=True)

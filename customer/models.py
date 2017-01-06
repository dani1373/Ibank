from __future__ import unicode_literals

from django.db import models

from bank.models import Branch
from employee.models import Employee
from profile.models import Profile


class Customer(models.Model):
    STATE_CHOICES = (
        ('A', 'Active'),
        ('W', 'Waiting'),
        ('D', 'Disable'),
    )

    profile = models.OneToOneField(Profile)

    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='W')


class Account(models.Model):
    STATE_CHOICES = (
        ('A', 'Active'),
        ('D', 'Disable'),
    )

    customer = models.ForeignKey(Customer)

    branch = models.ForeignKey(Branch)
    creator = models.ForeignKey(Employee)

    account_number = models.CharField(max_length=10, null=False, blank=False, db_index=True, unique=True)
    credit = models.PositiveIntegerField(default=0, db_index=True)

    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='A')

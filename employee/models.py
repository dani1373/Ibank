from __future__ import unicode_literals

from django.db import models

from bank.models import Branch
from profile.models import Profile


class Employee(models.Model):
    TYPE_CHOICES = (
        ('N', 'Unknown'),
        ('L', 'Lawyer'),
        ('C', 'Cashier'),
        ('A', 'Auditor'),
        ('T', 'ATM Master'),
    )

    profile = models.OneToOneField(Profile)
    branch = models.ForeignKey(Branch, null=False, blank=False, db_index=True)

    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='N', null=False, blank=False, db_index=True)

    def get_type(self):
        return self.get_type_display()

from __future__ import unicode_literals

from django.db import models

from profile.models import Profile


class Employee(models.Model):
    TYPE_CHOICES = (
        ('L', 'Lawyer'),
        ('C', 'Cashier'),
        ('A', 'Auditor'),
        ('T', 'ATM Master'),
    )

    profile = models.ForeignKey(Profile)

    type = models.CharField(max_length=1, choices=TYPE_CHOICES, null=False, blank=False, db_index=True)

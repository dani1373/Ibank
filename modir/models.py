from __future__ import unicode_literals

from django.db import models

from profile.models import Profile


class BankAdmin(models.Model):
    profile = models.ForeignKey(Profile)


class BranchAdmin(models.Model):
    profile = models.ForeignKey(Profile)

from __future__ import unicode_literals

from django.db import models

from profile.models import Profile


class BankAdmin(models.Model):
    profile = models.OneToOneField(Profile)

    def get_type(self):
        return 'Bank Admin'


class BranchAdmin(models.Model):
    profile = models.OneToOneField(Profile)

    def get_type(self):
        return 'Branch Admin'

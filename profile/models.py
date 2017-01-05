from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User)

    address = models.CharField(max_length=100, null=False, blank=False)
    national_id = models.CharField(max_length=10, unique=True, null=False, blank=False, db_index=True)
    phone_number = models.CharField(max_length=11, null=False, blank=False, db_index=True)

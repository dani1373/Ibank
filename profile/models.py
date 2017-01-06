from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User)

    password = models.CharField(max_length=10, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    national_id = models.CharField(max_length=10, unique=True, null=False, blank=False, db_index=True)
    phone_number = models.CharField(max_length=11, null=False, blank=False, db_index=True)

    def get_type(self):
        if hasattr(self, 'bankadmin'):
            return self.bankadmin.get_type()
        if hasattr(self, 'branchadmin'):
            return self.branchadmin.get_type()
        if hasattr(self, 'employee'):
            return self.employee.get_type()

    @staticmethod
    def register(data):
        first_name = data['first_name']
        last_name = data['last_name']
        national_id = data['national_id']
        phone_number = data['phone_number']
        address = data['address']

        if Profile.objects.filter(national_id=national_id).exists():
            return Profile.objects.get(national_id=national_id)

        user = User.objects.create(first_name=first_name, last_name=last_name, username=national_id)
        password = str(uuid.uuid4())[:6]
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(user=user, phone_number=phone_number, address=address, national_id=national_id,
                                         password=password)

        return profile

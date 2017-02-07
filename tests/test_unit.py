import unittest

from django.contrib import auth

from modir.models import BankAdmin
from profile.models import Profile


class SampleTest(unittest.TestCase):
    def setUp(self):
        data = dict()

        data['first_name'] = 'Modir'
        data['last_name'] = 'Ibank'
        data['national_id'] = '1234567890'
        data['phone_number'] = '0912345678'
        data['address'] = 'hichja'
        data['email'] = 'sadfall95ibank@gmail.com'

        profile = Profile.register(data=data)
        profile.user.set_password('123456')
        profile.user.save()
        profile.password = '123456'
        profile.save()

    def test_profileRegister(self):
        self.assertIn(Profile.objects.all()[0].user.first_name, 'Modir')

    def test_bankAdminRegister(self):
        BankAdmin.objects.create(profile = Profile.objects.all()[0])
        self.assertEqual(Profile.objects.all()[0], BankAdmin.objects.all()[0].profile)

    def test_profileIntegrity(self):
        self.assertEqual(Profile.objects.all()[0].get_type(), 'Bank Admin')

    def test_bankAdminType(self):
        self.assertEqual(BankAdmin.objects.all()[0].get_type(), 'Bank Admin')

    def test_authorization(self):
        user = auth.authenticate(username='1234567890', password='123456')
        self.assertNotEqual(user, None)

    def test_session(self):
        user = auth.authenticate(username='1234567890', password='123456')
        self.assertEqual(user.is_authenticated(), True)

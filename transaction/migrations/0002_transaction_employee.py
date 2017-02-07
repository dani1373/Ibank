# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-07 19:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.Employee'),
        ),
    ]
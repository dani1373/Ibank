# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-07 13:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('modir', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annual_profit', models.FloatField(default=0)),
                ('card_commission', models.PositiveIntegerField(default=0)),
                ('cheque_commission', models.PositiveIntegerField(default=0)),
                ('sms_commission', models.PositiveIntegerField(default=0)),
                ('card_to_card_commission', models.PositiveIntegerField(default=0)),
                ('transfer_commission', models.PositiveIntegerField(default=0)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='modir.BankAdmin')),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('admin', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='modir.BranchAdmin')),
            ],
        ),
    ]

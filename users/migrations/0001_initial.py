# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-07 05:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('fullname', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('occupation', models.CharField(max_length=50)),
                ('mobile', models.IntegerField()),
                ('email', models.EmailField(max_length=30)),
                ('pin', models.CharField(max_length=50)),
                ('national_id', models.IntegerField(primary_key=True, serialize=False)),
                ('nationality', models.CharField(max_length=50)),
                ('physical_address', models.CharField(max_length=50)),
                ('box', models.IntegerField()),
                ('code', models.IntegerField()),
                ('town', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('status', models.CharField(default='active', max_length=20)),
            ],
            options={
                'db_table': 'Users',
            },
        ),
    ]

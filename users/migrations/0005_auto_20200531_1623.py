# Generated by Django 3.0.6 on 2020-05-31 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200531_1529'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='uuid',
            new_name='transaction_id',
        ),
    ]

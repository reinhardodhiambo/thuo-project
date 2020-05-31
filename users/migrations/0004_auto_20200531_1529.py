# Generated by Django 3.0.6 on 2020-05-31 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_users_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='box',
        ),
        migrations.RemoveField(
            model_name='users',
            name='code',
        ),
        migrations.RemoveField(
            model_name='users',
            name='nationality',
        ),
        migrations.RemoveField(
            model_name='users',
            name='occupation',
        ),
        migrations.RemoveField(
            model_name='users',
            name='physical_address',
        ),
        migrations.RemoveField(
            model_name='users',
            name='town',
        ),
        migrations.AlterField(
            model_name='users',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='gender',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

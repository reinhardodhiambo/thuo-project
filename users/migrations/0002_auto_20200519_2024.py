# Generated by Django 3.0.6 on 2020-05-19 17:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='user_type',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='box',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='code',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='mobile',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='nationality',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='occupation',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='users',
            name='physical_address',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='pin',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='town',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

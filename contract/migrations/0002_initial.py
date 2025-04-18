# Generated by Django 5.1.1 on 2025-03-05 12:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contract', '0001_initial'),
        ('property', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='contractmodel',
            name='apartment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='property.apartmentmodel'),
        ),
        migrations.AddField(
            model_name='contractmodel',
            name='landlord',
            field=models.ManyToManyField(default=[], related_name='tenant_contracts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contractmodel',
            name='tenant',
            field=models.ManyToManyField(default=[], related_name='landlord_contracts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payedmodel',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract.contractmodel'),
        ),
    ]

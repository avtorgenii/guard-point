# Generated by Django 5.1.4 on 2025-01-06 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security_hub', '0004_remove_worker_scan_scanlog_worker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scanlog',
            name='type',
        ),
        migrations.AddField(
            model_name='scanlog',
            name='scan_result',
            field=models.BooleanField(choices=[(True, 'Successful'), (False, 'Denied')], null=True),
        ),
        migrations.AddField(
            model_name='scanlog',
            name='scan_type',
            field=models.BooleanField(choices=[(True, 'Entrance'), (False, 'Exit')], null=True),
        ),
    ]

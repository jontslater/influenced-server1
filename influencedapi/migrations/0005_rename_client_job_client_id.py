# Generated by Django 4.1.3 on 2024-08-13 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('influencedapi', '0004_remove_job_client_id_job_client'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='client',
            new_name='client_id',
        ),
    ]

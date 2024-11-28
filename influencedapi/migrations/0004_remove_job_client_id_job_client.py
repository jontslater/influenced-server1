# Generated by Django 4.1.3 on 2024-08-13 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('influencedapi', '0003_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='client_id',
        ),
        migrations.AddField(
            model_name='job',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='influencedapi.user'),
            preserve_default=False,
        ),
    ]
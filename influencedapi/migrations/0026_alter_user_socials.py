# Generated by Django 4.1.3 on 2025-01-04 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('influencedapi', '0025_alter_social_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='socials',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='influencedapi.social'),
        ),
    ]
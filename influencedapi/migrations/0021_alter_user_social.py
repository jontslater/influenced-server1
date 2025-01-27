# Generated by Django 4.1.3 on 2024-12-03 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('influencedapi', '0020_social_user_alter_user_social'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='social',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_profiles', to='influencedapi.social'),
        ),
    ]

# Generated by Django 5.1.6 on 2025-03-10 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='userprofile',
            index=models.Index(fields=['email'], name='user_profil_email_27350e_idx'),
        ),
        migrations.AddIndex(
            model_name='userprofile',
            index=models.Index(fields=['phone_number'], name='user_profil_phone_n_01ef8e_idx'),
        ),
        migrations.AddIndex(
            model_name='userprofile',
            index=models.Index(fields=['created_at'], name='user_profil_created_991e13_idx'),
        ),
    ]

# Generated by Django 4.0.2 on 2022-11-08 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_remove_notes_password_notes_access'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='access',
        ),
        migrations.AddField(
            model_name='notes',
            name='password',
            field=models.TextField(default='ZekDcuDHBuzmPmf'),
        ),
    ]

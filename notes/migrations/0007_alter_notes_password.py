# Generated by Django 4.0.2 on 2023-08-18 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_alter_notes_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='password',
            field=models.TextField(default='jDEzLXCFGuNXjRm'),
        ),
    ]

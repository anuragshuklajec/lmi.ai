# Generated by Django 5.0.2 on 2024-02-28 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lmiApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='CustomUser',
        ),
    ]

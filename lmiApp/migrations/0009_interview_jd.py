# Generated by Django 5.0.2 on 2024-03-16 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmiApp', '0008_alter_interviewdetail_expiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='jd',
            field=models.TextField(default='Fill this'),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.0.2 on 2024-03-16 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmiApp', '0009_interview_jd'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='role',
            field=models.CharField(default='Django developer', max_length=50),
            preserve_default=False,
        ),
    ]

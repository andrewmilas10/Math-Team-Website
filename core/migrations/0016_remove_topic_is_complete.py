# Generated by Django 2.1.7 on 2019-05-09 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_topic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='is_complete',
        ),
    ]

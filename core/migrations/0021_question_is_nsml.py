# Generated by Django 2.1.7 on 2019-06-12 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20190606_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_NSML',
            field=models.BooleanField(default=True),
        ),
    ]
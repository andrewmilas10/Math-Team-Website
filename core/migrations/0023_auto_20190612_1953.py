# Generated by Django 2.1.7 on 2019-06-13 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20190612_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='testProgress',
            field=models.CharField(default='{"2016 Advanced Geometrical Concepts": 0,"2016 Ratios, Proportions and Percents": 0,"RAND Ratios, Proportions and Percents": 0}', max_length=9999),
        ),
    ]
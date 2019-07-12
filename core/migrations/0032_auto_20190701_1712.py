# Generated by Django 2.1.7 on 2019-07-01 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20190627_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='testQuestion',
            field=models.CharField(default='{"2016 Advanced Geometrical Concepts": ["", "", "", "", ""],"2016 Ratios, Proportions and Percents": ["", "", "", "", ""],"RAND Ratios, Proportions and Percents": ["", "", "", "", ""],"2012 Number Bases": ["", "", "", "", ""],"2010 Number Bases": ["", "", "", "", ""],"2008 Number Bases": ["", "", "", "", ""],"RAND Number Bases": ["", "", "", "", ""]}', max_length=99999),
        ),
        migrations.AlterField(
            model_name='profile',
            name='testAnswers',
            field=models.CharField(default='{"2016 Advanced Geometrical Concepts": ["", "", "", "", ""],"2016 Ratios, Proportions and Percents": ["", "", "", "", ""],"RAND Ratios, Proportions and Percents": ["", "", "", "", ""],"2012 Number Bases": ["", "", "", "", ""],"2010 Number Bases": ["", "", "", "", ""],"2008 Number Bases": ["", "", "", "", ""],"RAND Number Bases": ["", "", "", "", ""]}', max_length=999),
        ),
        migrations.AlterField(
            model_name='profile',
            name='testDistribution',
            field=models.CharField(default='{"2016 Advanced Geometrical Concepts": [0, 0, 0, 0, 0],"2016 Ratios, Proportions and Percents": [0, 0, 0, 0, 0],"RAND Ratios, Proportions and Percents": [0, 0, 0, 0, 0],"2012 Number Bases": [0, 0, 0, 0, 0],"2010 Number Bases": [0, 0, 0, 0, 0],"2008 Number Bases": [0, 0, 0, 0, 0],"RAND Number Bases": [0, 0, 0, 0, 0]}', max_length=999),
        ),
        migrations.AlterField(
            model_name='profile',
            name='testProgress',
            field=models.CharField(default='{"2016 Advanced Geometrical Concepts": 0,"2016 Ratios, Proportions and Percents": 0,"RAND Ratios, Proportions and Percents": 0,"2012 Number Bases": 0,"2010 Number Bases": 0,"2008 Number Bases": 0,"RAND Number Bases": 0}', max_length=9999),
        ),
        migrations.AlterField(
            model_name='profile',
            name='testTime',
            field=models.CharField(default='{"2016 Advanced Geometrical Concepts": 0,"2016 Ratios, Proportions and Percents": 0,"RAND Ratios, Proportions and Percents": 0,"2012 Number Bases": 0,"2010 Number Bases": 0,"2008 Number Bases": 0,"RAND Number Bases": 0}', max_length=99999999999),
        ),
    ]

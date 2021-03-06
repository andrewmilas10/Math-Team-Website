# Generated by Django 2.1.7 on 2019-06-13 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_question_is_nsml'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='progress',
        ),
        migrations.AddField(
            model_name='profile',
            name='testProgress',
            field=models.CharField(default='{"Ratios, Proportions and Percents": 0,"Number Theory and Divisibility": 0,"Counting Basics and Probability": 0,"Quadratics": 0,"Freshman Conference": 0,"Probability": 0,"Advanced Geometrical Concepts": 0,"Perimeter, Area and Surface Area": 0,"Logic, Sets and Venn Diagram": 0,"Similarity": 0,"Coordinate Geometry": 0,"Circles": 0,"Sophomore Conference": 0,"Trigonometry": 0,"Junior Conference": 0,"Parametric Equations": 0,"Theory of Equations": 0,"Senior Conference": 0,"Freshman Regionals": 0,"Freshman State": 0,"Sophomore Regionals": 0,"Sophomore State": 0,"Junior Regionals": 0,"Junior State": 0,"Senior Regionals": 0,"Senior State": 0}', max_length=9999),
        ),
        migrations.AddField(
            model_name='question',
            name='calc_allowed',
            field=models.BooleanField(default=False),
        ),
    ]

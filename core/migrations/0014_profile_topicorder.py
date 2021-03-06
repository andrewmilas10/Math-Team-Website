# Generated by Django 2.1.7 on 2019-05-09 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20190505_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='topicOrder',
            field=models.CharField(default='{"Ratios, Proportions and Percents": 0,"Number Theory and Divisibility": 1,"Counting Basics and Probability": 2,"Quadratics": 3,"Probability": 4,"Advanced Geometrical Concepts": 5,"Perimeter, Area and Surface Area": 6,"Logic, Sets and Venn Diagram": 7,"Similarity": 8,"Coordinate Geometry": 9,"Circles": 10,"Trigonometry": 11,"Parametric Equations": 12,"Theory of Equations": 13,"Freshman Regionals": 14,"Freshman State": 15,"Sophomore Regionals": 16,"Sophomore State": 17,"Junior Regionals": 18,"Junior State": 19,"Senior Regionals": 20,"Senior State": 21}', max_length=1000),
        ),
    ]

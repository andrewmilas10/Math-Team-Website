# Generated by Django 2.1.7 on 2019-05-01 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_profile_currcorrect'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='currCorrect',
            field=models.CharField(default='{"Ratios, Proportions and Percents": "F","Number Theory and Divisibility": "F","Counting Basics and Probability": "F","Quadratics": "F","Probability": "F","Advanced Geometrical Concepts": "F","Perimeter, Area and Surface Area": "F","Logic, Sets and Venn Diagram": "F","Similarity": "F","Coordinate Geometry": "F","Circles": "F","Trigonometry": "F","Parametric Equations": "F","Theory of Equations": "F"}', max_length=1000),
        ),
    ]

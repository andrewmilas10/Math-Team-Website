from django.db import models
# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#this function handles all of the posts on the website. when an admin makes a new post, these are all of the
#variables for each object
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

#as for the post, the variables for questions are listed here and when admins make a new question,
#it receives all of the parameters from here.
class Question(models.Model):
    GRADES_LIST = (
        ('Freshman', 'Freshman'),
        ('Sophomore', 'Sophomore'),
        ('Junior', 'Junior'),
        ('Senior', 'Senior'),
    )
    TOPIC_LIST = (
        ('Ratios, Proportions and Percents', 'Ratios, Proportions and Percents'),
        ('Number Theory and Divisibility', 'Number Theory and Divisibility'),
        ('Counting Basics and Probability', 'Counting Basics and Probability'),
        ('Quadratics', 'Quadratics'),
        ('Probability', 'Probability'),
        ('Advanced Geometrical Concepts', 'Advanced Geometrical Concepts'),
        ('Perimeter, Area and Surface Area', 'Perimeter, Area and Surface Area'),
        ('Logic, Sets and Venn Diagram', 'Logic, Sets and Venn Diagram'),
        ('Similarity', 'Similarity'),
        ('Coordiante Geometry', 'Coordiante Geometry'),
        ('Circles', 'Circles'),
        ('Trigonometry', 'Trigonometry'),
        ('Parametric Equations', 'Parametric Equations'),
        ('Theory of Equations', 'Theory of Equations'),
    )
    QUESTION_NUMBERS = (
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5')
    )
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    grade = models.CharField(max_length=9, choices=GRADES_LIST, default='Freshman')
    topic = models.CharField(max_length=100, choices=TOPIC_LIST, default='Ratios, Proportions and Percents')
    description = models.TextField(default="", blank=True)
    answer = models.CharField(max_length=250, default="1")
    questionPicture = models.FileField()
    answerPicture = models.FileField()
    difficulty = models.CharField(max_length=3, choices=QUESTION_NUMBERS, default='1')
    year = models.CharField(max_length=250)
    created_date = models.DateTimeField(
            default=timezone.now)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.topic + " " + self.year

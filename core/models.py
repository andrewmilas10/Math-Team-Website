from django.db import models
# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    TOPIC_LIST = (
        'Ratios, Proportions and Percents',
        'Number Theory and Divisibility',
        'Counting Basics and Probability',
        'Quadratics',
        'Freshman Conference',
        'Probability',
        'Advanced Geometrical Concepts',
        'Perimeter, Area and Surface Area',
        'Logic, Sets and Venn Diagram',
        'Similarity',
        'Coordinate Geometry',
        'Circles',
        'Sophomore Conference',
        'Trigonometry',
        'Junior Conference',
        'Parametric Equations',
        'Theory of Equations',
        'Senior Conference',
        'Freshman Regionals',
        'Freshman State',
        'Sophomore Regionals',
        'Sophomore State',
        'Junior Regionals',
        'Junior State',
        'Senior Regionals',
        'Senior State'
    )

    PROGRESS_OPTIONS = (
        (0, 0),
        (10, 10),
        (20, 20),
        (30, 30),
        (40, 40),
        (50, 50),
        (60, 60),
        (70, 70),
        (80, 80),
        (90, 90),
        (100, 100)
    )

    progress = models.IntegerField(choices=PROGRESS_OPTIONS, default=0)
    topicDict = "{"
    topicDict2 = "{"
    topicDict3 = "{"
    topicDict4 = "{"
    topicDict4 = "{"
    topicDict5 = "{"
    i = 0
    for topic in TOPIC_LIST:
        topicDict+= "\"" + topic+"\": 0,"
        topicDict2 += "\"" + topic + "\": 3,"
        topicDict3 += "\"" + topic + "\": \"N\","
        topicDict4 += "\"" + topic + "\": \"F\","
        topicDict5 += "\"" + topic + "\": " + str(i) + ","
        i+=1

    topicDict = topicDict[:-1]+"}"
    topicDict2 = topicDict2[:-1] + "}"
    topicDict3 = topicDict3[:-1] + "}"
    topicDict4 = topicDict4[:-1] + "}"
    topicDict5 = topicDict5[:-1] + "}"
    progress2 = models.CharField(max_length=1000, default=topicDict)
    attempts = models.CharField(max_length=1000, default=topicDict2)
    currQuestions = models.CharField(max_length=1000, default=topicDict3)
    currCorrect = models.CharField(max_length=1000, default=topicDict4)
    topicOrder = models.CharField(max_length=1000, default=topicDict5)


    def __str__(self):
        return self.user.username + " Profile"

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

#this function handles all of the posts on the website. when an admin makes a new post, these are all of the
#variables for each object
class Topic(models.Model):
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
        ('Coordinate Geometry', 'Coordinate Geometry'),
        ('Circles', 'Circles'),
        ('Trigonometry', 'Trigonometry'),
        ('Parametric Equations', 'Parametric Equations'),
        ('Theory of Equations', 'Theory of Equations'),
        ('Freshman Regionals', 'Freshman Regionals'),
        ('Freshman State', 'Freshman State'),
        ('Sophomore Regionals', 'Sophomore Regionals'),
        ('Sophomore State', 'Sophomore State'),
        ('Junior Regionals', 'Junior Regionals'),
        ('Junior State', 'Junior State'),
        ('Senior Regionals', 'Senior Regionals'),
        ('Senior State', 'Senior State')
    )

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    grade = models.CharField(max_length=9, choices=GRADES_LIST, default='Freshman')
    topic = models.CharField(max_length=100, choices=TOPIC_LIST, default='Ratios, Proportions and Percents')
    description = models.TextField(default="", blank=True)
    firstFile = models.FileField()
    secondFile = models.FileField()
    thirdFile = models.FileField()
    created_date = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return self.topic

    def publish(self):
        self.published_date = timezone.now()
        self.save()

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
        ('Coordinate Geometry', 'Coordinate Geometry'),
        ('Circles', 'Circles'),
        ('Trigonometry', 'Trigonometry'),
        ('Parametric Equations', 'Parametric Equations'),
        ('Theory of Equations', 'Theory of Equations'),
        ('Freshman Regionals', 'Freshman Regionals'),
        ('Freshman State','Freshman State'),
        ('Sophomore Regionals','Sophomore Regionals'),
        ('Sophomore State','Sophomore State'),
        ('Junior Regionals','Junior Regionals'),
        ('Junior State','Junior State'),
        ('Senior Regionals','Senior Regionals'),
        ('Senior State','Senior State')
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

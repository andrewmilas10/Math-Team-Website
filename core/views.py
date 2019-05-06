from django.shortcuts import render, get_object_or_404
from .models import Post
from .models import Question
from .models import Profile
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm
import json
import operator
import random
from django.http import JsonResponse
from django.db.models import Q


def index(request):
    return render(request, 'core/index.html', {})

def post_list(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = Post.objects.all().order_by('published_date')
    return render(request, 'core/post_list.html', {'posts': posts, "activeNav": "1"})

def learn(request, category, title):
    global activeNav;
    activeNav = "5"
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = Post.objects.all().order_by('published_date')
    return render(request, 'core/learn.html', {'posts': posts, "title": title, "activeNav": "5"})

#this is the function that is loaded when the list of questions is called, it also works on the search functionality of the
#website by finding the questions under the filter with a serach query
def question_list(request):
    topiclist = ['Ratios, Proportions and Percents','Number Theory and Divisibility','Counting Basics and Probability'
    , 'Quadratics', 'Probability', 'Advanced Geometrical Concepts', 'Perimeter, Area and Surface Area',
    'Logic, Sets and Venn Diagram', 'Similarity', 'Coordinate Geometry', 'Circles', 'Trigonometry',
    'Parametric Equations', 'Theory of Equations']
    grades = ['Freshman', 'Sophomore', 'Junior', 'Senior']
    questionNumbers= ['1','2','3','4','5']
    topicsSearched=[]
    gradesSearched = []
    numberSearched = []
    if not request.user.is_authenticated:
        return render(request, 'core/login.html')
    else:
        question_results = Question.objects.all()
        questions = Question.objects.all()
        for topic in topiclist:
            button = request.POST.get(topic)
            if button:
                topicsSearched.append(topic)
        for grade in grades:
            button = request.POST.get(grade)
            if button:
                gradesSearched.append(grade)
        for number in questionNumbers:
            button = request.POST.get(number)
            if button:
                numberSearched.append(number)
        print(gradesSearched)
        print(numberSearched)
        print(topicsSearched)
        if topicsSearched or gradesSearched or numberSearched:
            if topicsSearched:
                question_results = question_results.filter(topic__in=topicsSearched)
            if gradesSearched:
                question_results = question_results.filter(grade__in=gradesSearched)
            if numberSearched:
                question_results = question_results.filter(difficulty__in=numberSearched)
            return render(request, 'core/questions.html', {'questions': questions,'question_results': question_results, "activeNav": "2"})


        return render(request, 'core/question_list.html', {'questions': questions,"activeNav": "2"})



#this function returns the question object to the details page as well as checks the
#answer of the users input to see if the user got it right or not. it also checks if the
#user has completed the question or not
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    submitbutton= request.POST.get('submit')
    submitAnswerButton = request.POST.get('submitAnswer')
    correctAnswer = False
    if submitbutton:
        context={
        'submitbutton': submitbutton,
        'question': question,
        "activeNav": "2"
        }
        return render(request, 'core/question_detail.html', context)
    elif submitAnswerButton:
        input = request.POST.get('answer')
        question.is_complete=True
        question.save()
        if input == question.answer:
            correctAnswer = True
        context={
            'submitAnswerButton': submitAnswerButton,
            'question': question,
            'correctAnswer': correctAnswer,
            "activeNav": "2"
        }
        return render(request, 'core/question_detail.html', context)
    else:
        return render(request, 'core/question_detail.html', {'question': question, "activeNav": "0"})


#this function handles the creating of a new user
class UserFormView(View):
    form_class = UserForm
    template_name = 'core/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()

            Profile.objects.create(user=user, progress= 0)

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'core/homepage_logged_in.html', {"activeNav": "0"})
        return render(request, 'core/registration_form.html', {'form': form, 'error_message': 'your username or email may already be registered. please choose another one'})


#this function logs the user out of the page and returns the user back to the login page
def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'core/login.html', context)

#this function logs the user in to the website and redirects them to the homepage for logged in users
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                questions = Question.objects.all()
                return render(request, 'core/homepage_logged_in.html', {'questions': questions, "activeNav": "0"})
            else:
                return render(request, 'core/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'core/login.html', {'error_message': 'Invalid login'})
    return render(request, 'core/login.html')

def homepage(request):
    return render(request, 'core/homepage_logged_in.html', {"activeNav": "0"})

def pickColor(progress):
    if progress >= 90:
        return "progress-bar progress-bar-striped"
    elif progress >= 70:
        return "progress-bar-striped bg-success"
    elif progress >= 30:
        return "progress-bar-striped bg-warning"
    else:
        return "progress-bar-striped bg-danger"

activeNav = "3";
def practice_topics(request, category, title):
    # topiclist = ['Ratios, Proportions and Percents', 'Number Theory and Divisibility', 'Counting Basics and Probability'
    #     , 'Quadratics', 'Probability', 'Advanced Geometrical Concepts', 'Perimeter, Area and Surface Area',
    #              'Logic, Sets and Venn Diagram', 'Similarity', 'Coordinate Geometry', 'Circles', 'Trigonometry',
    #              'Parametric Equations', 'Theory of Equations']
    global activeNav;
    if category == "0":
        activeNav = "3";
        topiclist = ['Ratios, Proportions and Percents', 'Number Theory and Divisibility',
                     'Counting Basics and Probability', 'Quadratics']
    elif category == "1":
        activeNav = "3";
        topiclist = ['Geometric Probability', 'Advanced Geometrical Concepts', 'Perimeter, Area, and Surface Area',
                     'Logic, Sets, and Venn Diagram', 'Similarity', 'Coordinate Geometry', 'Circles']
    elif category == "2":
        activeNav = "3";
        topiclist = ['Probability', 'Coordinate Geometry', 'Trigonometry']
    elif category == "3":
        activeNav = "3";
        topiclist = ['Trigonometry', 'Parametric Equations', 'Theory of Equations']
    elif category == "4":
        activeNav = "4";
        topiclist = ["Freshman Regionals", "Freshman State"]
    elif category == "5":
        activeNav = "4";
        topiclist = ["Sophomore Regionals", "Sophomore State"]
    elif category == "6":
        activeNav = "4";
        topiclist = ["Junior Regionals", "Junior State"]
    elif category == "7":
        activeNav = "4";
        topiclist = ["Senior Regionals", "Senior State"]
    user = request.user
    progressDict = json.loads(user.profile.progress2)
    progress = []
    for num in reversed(sorted(progressDict.items(), key=operator.itemgetter(1))):
        if (num[0] in topiclist):
            progress.append([num[0], num[1], pickColor(num[1])])
    return render(request, 'core/practice_topics.html', {'title': title, 'category': category, 'progress': progress, 'topics': topiclist, "activeNav": activeNav})

def pickQuestion(topic, difficulties):
    possQuestions = Question.objects.filter(is_complete=False).filter(topic=topic).filter(difficulty__in=difficulties)

    if not possQuestions.exists():
        totalPoss = Question.objects.filter(topic=topic).filter(difficulty__in=difficulties)
        for poss in totalPoss:
            poss.is_complete = False
            poss.save()
        possQuestions = Question.objects.filter(is_complete=False).filter(topic=topic).filter(difficulty__in=difficulties)

    for quest in possQuestions:
        print(quest.answer)

    question = random.choice(possQuestions)
    question.is_complete = True
    question.save()
    return question

def reset(request, topic, category, title):
    global activeNav;
    user = request.user
    progressDict = json.loads(user.profile.progress2)
    progressDict[topic] = 0
    user.profile.progress2 = json.dumps(progressDict)
    user.profile.save()
    return practice_topics(request, category, title)

def practice_topics_detail(request, topic):
    global activeNav;
    user = request.user
    progressDict = json.loads(user.profile.progress2)
    attemptsDict = json.loads(user.profile.attempts)
    currCorrectDict = json.loads(user.profile.currCorrect)

    questionsIDsDict = json.loads(user.profile.currQuestions)
    if (questionsIDsDict[topic] == "N"):
        pastQuestion = pickQuestion(topic, [1, 2])
        user.profile.currQuestions = json.dumps(questionsIDsDict)
        user.profile.save()
    else:
        pastQuestion = Question.objects.get(id = questionsIDsDict[topic])

    submitAnswerButton = request.POST.get('submitAnswer')
    nextQuestionButton = request.POST.get('nextQuestion')
    showSolutionButton = request.POST.get('showSolution')
    correctAnswer = False

    def getContext():
        return {
            'progress2': progressDict[topic],
            'attempts': attemptsDict[topic],
            'color': pickColor(progressDict[topic]),
            'topic': topic,
            'showSolutionButton': showSolutionButton,
            'question': pastQuestion,
            'correctAnswer': correctAnswer,
            "activeNav": activeNav
        }

    if showSolutionButton:
        return render(request, 'core/practice_topics_detail.html', getContext())
    elif nextQuestionButton and (currCorrectDict[topic] == "T" or attemptsDict[topic]==0):
        attemptsDict[topic] = 3
        currCorrectDict[topic] = "F"
        user.profile.attempts = json.dumps(attemptsDict)
        user.profile.currCorrect = json.dumps(currCorrectDict)
        # pastQuestion.is_complete = True
        # pastQuestion.save()

        if progressDict[topic] <= 50:
            difficulties = [1, 2, 3]
        else:
            difficulties = [4, 5]

        pastQuestion = pickQuestion(topic, difficulties)
        questionsIDsDict[topic] = pastQuestion.id
        user.profile.currQuestions = json.dumps(questionsIDsDict)
        user.profile.save()
        return render(request, 'core/practice_topics_detail.html', getContext())
    elif currCorrectDict[topic] == "T":
        correctAnswer = True
        return render(request, 'core/practice_topics_detail.html', getContext())
    elif submitAnswerButton:
        input = request.POST.get('answer')
        if input.replace(" ", "") in pastQuestion.answer.replace(" ", "").split("@"):
            correctAnswer = True
            progressDict[topic] += 10
            if (progressDict[topic]) > 100:
                progressDict[topic] = 100
            currCorrectDict[topic] = "T"
            user.profile.progress2 = json.dumps(progressDict)
            user.profile.currCorrect = json.dumps(currCorrectDict)
            user.profile.save()
        else:
            attemptsDict[topic] -= 1
            if attemptsDict[topic] == 0:
                progressDict[topic]-=15
            if (progressDict[topic]) < 0:
                progressDict[topic] = 0
            user.profile.progress2 = json.dumps(progressDict)
            user.profile.attempts = json.dumps(attemptsDict)
            user.profile.save()
        return render(request, 'core/practice_topics_detail.html', getContext())
    else:
        return render(request, 'core/practice_topics_detail.html', getContext())

def questions(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'core/login.html')
    else:
        try:
            question_ids = []
            for question in Question.objects.filter(user=request.user):
                question_ids.append(question.pk)
            users_questions = Question.objects.filter(pk__in=question_ids)
        except Question.DoesNotExist:
            users_questions = []
        return render(request, 'core/questions.html', {
            'question_list': users_questions,
            'filter_by': filter_by,
            "activeNav": "2"
        })

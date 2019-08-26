from django.shortcuts import render, get_object_or_404
from .models import Post
from .models import Question
from .models import Profile
from .models import Topic
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth.models import User
import json
import operator
import random
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q

topics = [['Ratios, Proportions and Percents', 'Number Theory and Divisibility', 'Counting Basics and Probability', 'Number Bases', 'Quadratics', 'Freshman Conference'],
          ['Geometric Probability', 'Functions', 'Advanced Geometrical Concepts', 'Perimeter, Area, and Surface Area',
                     'Logic, Sets, and Venn Diagram', 'Similarity', 'Coordinate Geometry', 'Circles', 'Sophomore Conference'],
          ['Probability', 'Trigonometry', 'Polynomials', 'Logs and Exponents', 'Transformations using Matrices', 'Junior Conference'],
          ['Trigonometry', 'Parametric Equations', 'Theory of Equations', 'Sequences and Series', 'Vectors', 'Senior Conference'],
          ["Freshman Regionals", "Freshman State"],
          ["Sophomore Regionals", "Sophomore State"],
          ["Junior Regionals", "Junior State"],
          ["Senior Regionals", "Senior State"]]

activeNavs = ["3", "3", "3", "3", "4", "4", "4", "4"]
titles = ['Freshman Topics', 'Sophomore Topics', 'Junior Topics', 'Senior Topics', 'Freshman Regionals/State',  'Sophomore Regionals/State',  'Junior Regionals/State',  'Senior Regionals/State']

def index(request):
    return render(request, 'core/index.html', {})

def post_list(request):
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = Post.objects.all().order_by('published_date')
    return render(request, 'core/post_list.html', {'posts': posts, "activeNav": "1"})

def learn(request, category, title):
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
    global activeNav, topics;
    activeNav = "5"
    category = int(category)
    topiclist = topics[category]
    allTopics = Topic.objects.all()
    topicDesriptions = []
    for top in allTopics:
        if (top.topic in topiclist):
            topicDesriptions.append([top.topic, top.description, top.firstFile, top.secondDescription, top.secondFile,
                                     top.thirdDescription, top.thirdFile, top.fourthDescription])

    return render(request, 'core/learn.html', {'topicDescriptions': topicDesriptions, "title": title, "activeNav": "5"})

def progress(request, category, title):
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
    global activeNav, topics;
    activeNav = "7"
    category = int(category)
    topiclist = topics[category]

    user = request.user
    progressListDict = json.loads(user.profile.progress)
    topicDesriptions = []
    for topic in topiclist:
        possQuestions = Question.objects.filter(topic__in=[topic])
        if possQuestions.exists() or (topic in ['Freshman Conference', 'Sophomore Conference', 'Junior Conference','Senior Conference']):
            topicDesriptions.append([topic, progressListDict[topic]])
    return render(request, 'core/progress.html', {'topicDescriptions': topicDesriptions, "title": title, "activeNav": "7"})


    # topiclist = topics[category]
    # allTopics = Topic.objects.all()
    # topicDesriptions = []
    # for top in allTopics:
    #     if (top.topic in topiclist):
    #         topicDesriptions.append([top.topic, top.description, top.firstFile, top.secondDescription, top.secondFile,
    #                                  top.thirdDescription, top.thirdFile, top.fourthDescription])
    #
    # return render(request, 'core/progress.html', {'topicDescriptions': topicDesriptions, "title": title, "activeNav": "7"})

#this is the function that is loaded when the list of questions is called, it also works on the search functionality of the
#website by finding the questions under the filter with a serach query
def question_list(request):
    topiclist = ['Ratios, Proportions and Percents','Number Theory and Divisibility', "Number Bases", 'Counting Basics and Probability'
    , 'Quadratics', 'Probability', 'Advanced Geometrical Concepts', 'Perimeter, Area and Surface Area',
    'Logic, Sets and Venn Diagram', 'Similarity', 'Coordinate Geometry', 'Circles', 'Trigonometry',
    'Parametric Equations', 'Theory of Equations']
    grades = ['Freshman', 'Sophomore', 'Junior', 'Senior']
    questionNumbers= ['1','2','3','4','5']
    topicsSearched=[]
    gradesSearched = []
    numberSearched = []
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
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
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
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
        backBtn = request.POST.get("back")
        print(backBtn)
        if backBtn:
            return render(request, 'core/index.html')
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()

            Profile.objects.create(user=user)

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'core/homepage_logged_in.html', {"activeNav": "0"})
        return render(request, 'core/registration_form.html', {'form': form, 'error_message': 'Your username or email may already be registered. Please choose another one'})


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
    backBtn = request.POST.get("back")
    if backBtn:
        return render(request, 'core/index.html')
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
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
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
def practice_topics(request, category):
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
    global activeNav, activeNavs, topics, titles;
    category = int(category)
    activeNav = activeNavs[category]
    topiclist = topics[category]
    title = titles[category]

    user = request.user
    topicOrderDict = json.loads(user.profile.topicOrder)
    progress2 = json.loads(user.profile.progress2)
    progress = []
    for num in sorted(topicOrderDict.items(), key=operator.itemgetter(1)):
        if (num[0] in topiclist):
            possQuestions = Question.objects.filter(topic__in=[num[0]])
            if possQuestions.exists() or (num[0] in['Freshman Conference', 'Sophomore Conference', 'Junior Conference', 'Senior Conference'] ):
                progress.append([num[0], progress2[num[0]], pickColor(progress2[num[0]])])
    return render(request, 'core/practice_topics.html', {'title': title, 'category': category, 'progress': progress, 'topics': topiclist, "activeNav": activeNav})

def pickQuestion(topic, difficulties):
    if topic in ['Freshman Conference', 'Sophomore Conference', 'Junior Conference', 'Senior Conference']:
        topicList = topics[['Freshman Conference', 'Sophomore Conference', 'Junior Conference', 'Senior Conference'].index(topic)]
    else:
        topicList = [topic]
    # print(topicList)
    possQuestions = Question.objects.filter(is_complete=False).filter(topic__in=topicList).filter(difficulty__in=difficulties)
    print(possQuestions)
    if not possQuestions.exists():
        totalPoss = Question.objects.filter(topic__in=topicList).filter(difficulty__in=difficulties)
        for poss in totalPoss:
            poss.is_complete = False
            poss.save()
        possQuestions = Question.objects.filter(is_complete=False).filter(topic__in=topicList).filter(difficulty__in=difficulties)

    for quest in possQuestions:
        print(quest.answer)

    question = random.choice(possQuestions)
    question.is_complete = True
    question.save()
    return question

def reset(request, topic, category):
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
    global activeNav;
    user = request.user
    progressDict = json.loads(user.profile.progress2)
    progressListDict = json.loads(user.profile.progress)
    attemptsDict = json.loads(user.profile.attempts)
    currCorrectDict = json.loads(user.profile.currCorrect)
    questionsIDsDict = json.loads(user.profile.currQuestions)

    progressDict[topic] = 0
    progressListDict[topic].append(0);
    attemptsDict[topic] = 3
    currCorrectDict[topic] = "F"
    questionsIDsDict[topic] = "N"

    user.profile.progress2 = json.dumps(progressDict)
    user.profile.progress = json.dumps(progressListDict)
    user.profile.currQuestions = json.dumps(questionsIDsDict)
    user.profile.attempts = json.dumps(attemptsDict)
    user.profile.currCorrect = json.dumps(currCorrectDict)
    user.profile.save()

    return practice_topics(request, category)

def practice_topics_detail(request, topic):
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
    global activeNav;
    user = request.user
    progressDict = json.loads(user.profile.progress2)
    progressListDict = json.loads(user.profile.progress)
    attemptsDict = json.loads(user.profile.attempts)
    currCorrectDict = json.loads(user.profile.currCorrect)
    currAnswer = json.loads(user.profile.currAnswer)

    topicOrderDict = json.loads(user.profile.topicOrder)
    for top in topicOrderDict.keys():
        topicOrderDict[top]+=1
    topicOrderDict[topic] = 0
    user.profile.topicOrder = json.dumps(topicOrderDict)
    user.profile.save()

    questionsIDsDict = json.loads(user.profile.currQuestions)
    if (questionsIDsDict[topic] == "N"):
        pastQuestion = pickQuestion(topic, [1, 2])
        questionsIDsDict[topic] = pastQuestion.id
        user.profile.currQuestions = json.dumps(questionsIDsDict)
        user.profile.save()
    else:
        pastQuestion = Question.objects.get(id = questionsIDsDict[topic])

    submitAnswerButton = request.POST.get('submitAnswer')
    nextQuestionButton = request.POST.get('nextQuestion')
    backButton = request.POST.get('back')
    correctAnswer = False

    def getContext():
        return {
            'progress2': progressDict[topic],
            'attempts': attemptsDict[topic],
            'color': pickColor(progressDict[topic]),
            'topic': topic,
            'question': pastQuestion,
            'correctAnswer': correctAnswer,
            "activeNav": activeNav,
            "currAnswer": currAnswer[topic],
        }

    if backButton:
        category = 0
        while topic not in topics[category]:
            category += 1
        return practice_topics(request, str(category))
    elif nextQuestionButton and (currCorrectDict[topic] == "T" or attemptsDict[topic]==0):
        attemptsDict[topic] = 3
        currCorrectDict[topic] = "F"
        currAnswer[topic] = ""
        user.profile.attempts = json.dumps(attemptsDict)
        user.profile.currCorrect = json.dumps(currCorrectDict)
        user.profile.currAnswer = json.dumps(currAnswer)

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
        currAnswer[topic] = input
        user.profile.currAnswer = json.dumps(currAnswer)
        if input.replace(" ", "") in pastQuestion.answer.replace(" ", "").split("@"):
            correctAnswer = True
            progressDict[topic] += 10
            if (progressDict[topic]) > 100:
                progressDict[topic] = 100
            progressListDict[topic].append(progressDict[topic])
            currCorrectDict[topic] = "T"
            user.profile.progress2 = json.dumps(progressDict)
            user.profile.progress = json.dumps(progressListDict)
            user.profile.currCorrect = json.dumps(currCorrectDict)
            user.profile.save()
        else:
            attemptsDict[topic] -= 1
            if attemptsDict[topic] == 0:
                progressDict[topic]-=15
                progressListDict[topic].append(progressDict[topic])
            if (progressDict[topic]) < 0:
                progressDict[topic] = 0
                progressListDict[topic][-1] = 0
            user.profile.progress2 = json.dumps(progressDict)
            user.profile.progress = json.dumps(progressListDict)
            user.profile.attempts = json.dumps(attemptsDict)
            user.profile.save()
        return render(request, 'core/practice_topics_detail.html', getContext())
    else:
        return render(request, 'core/practice_topics_detail.html', getContext())

activeNav = "6";
def practice_tests(request, category):
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
    global activeNav, activeNavs, topics, titles;
    category = int(category)
    activeNav = "6"
    topiclist = topics[category]
    title = titles[category][:-6]+"Tests"

    user = request.user
    topicOrderDict = json.loads(user.profile.topicOrder)
    progress2 = json.loads(user.profile.progress2)
    progress = []
    for num in sorted(topicOrderDict.items(), key=operator.itemgetter(1)):
        if (num[0] in topiclist):
            possQuestions = Question.objects.filter(topic__in=[num[0]])
            if possQuestions.exists() or (num[0] in ['Freshman Conference', 'Sophomore Conference', 'Junior Conference','Senior Conference']):
                progress.append([num[0], progress2[num[0]], pickColor(progress2[num[0]])])
    return render(request, 'core/practice_tests.html', {'title': title, 'category': category, 'progress': progress, 'topics': topiclist, "activeNav": activeNav})

def practice_tests_detail(request, topic):
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
    global activeNav;
    user = request.user
    print(request.POST.get('answers'))
    testProgress = json.loads(user.profile.testProgress)
    testTime = json.loads(user.profile.testTime)
    testInfo = []
    for i in range(0, 5):
        if topic in topics[i]:
            category = i
            break

    for num in testProgress.items():
        print(num[0], num[0][5:], topic)
        if (num[0][5:] == topic):
            if num[0][:4] != "RAND" and Question.objects.filter(topic__in=[topic]).filter(year = num[0][:4])[0].calc_allowed:
                calcAllowed = "Calculator Allowed"
            elif num[0][:4] == "RAND":
                calcAllowed = "TODO, don't know yet"
            else:
                calcAllowed = "No Calculator"
            print(str(testTime[num[0]]))
            testInfo.append([num[0], str(num[1])+"/5", calcAllowed, str(testTime[num[0]])])

    return render(request, 'core/practice_tests_detail.html', {'title': topic, 'testInfo': testInfo, "activeNav": activeNav, "category": category})

def questions(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
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

def practice_tests_take(request, topic):
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
    global activeNav;
    user = request.user

    submitAnswersButton = request.POST.get('submitAnswers')
    backButton = request.POST.get('back')
    if backButton:
        return practice_tests_detail(request, topic[5:])
    if submitAnswersButton:
        answers = []
        for i in range(1, 6):
            answers.append(request.POST.get('answer'+str(i)))
        return submit_practice_test(request, topic, answers)

    testTime = json.loads(user.profile.testTime)
    currAnswers = json.loads(user.profile.testAnswers)
    currQuestions = json.loads(user.profile.testQuestion)
    if not request.POST.get('viewSolutions') and int(testTime[topic]) <= 0:
        currAnswers[topic] = ['', '', '', '', '']
        user.profile.testAnswers = json.dumps(currAnswers)
        if topic[:4] == "RAND":
            for i in range(1, 6):
                currQuestions[topic][i-1] = random.choice(Question.objects.filter(topic__in=[topic[5:]]).filter(difficulty=i)).id
        else:
            currQuestions[topic] = list(map(lambda x: x.id, sorted(Question.objects.filter(topic__in=[topic[5:]]).filter(year=topic[:4]), key=lambda t: t.difficulty)))
        user.profile.testQuestion = json.dumps(currQuestions)
        user.profile.save()

    questions = [get_object_or_404(Question, pk=currQuestions[topic][i]) for i in range(5)]

    if request.POST.get('viewSolutions'):
        return render(request, 'core/practice_tests_take.html',
                      {'viewSolutions': 1, 'title': topic, 'questions': questions, "activeNav": activeNav, "end": testTime[topic],
                       'currAnswers': str(currAnswers[topic])[1:-1], "distribution": str(json.loads(user.profile.testDistribution)[topic])[1:-1]})
    return render(request, 'core/practice_tests_take.html',
                  {'viewSolutions': 0, 'title': topic, 'questions': questions, "activeNav": activeNav, "end": testTime[topic],
                   'currAnswers': str(currAnswers[topic])[1:-1], "distribution": str(json.loads(user.profile.testDistribution)[topic])[1:-1]})

def start_timer(request):
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
    user = request.user
    testTime = json.loads(user.profile.testTime)
    testTime[request.POST.get('topic')] = request.POST.get('end')
    user.profile.testTime = json.dumps(testTime)
    user.profile.save()
    return HttpResponse()

def end_timer(request):
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
    text = submit_practice_test(request, request.POST.get('topic'), request.POST.get("answers").split(","))
    return HttpResponse(text)

def edit_answers(request):
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
    user = request.user
    testAnswers = json.loads(user.profile.testAnswers)
    testAnswers[request.POST.get('topic')][int(request.POST.get('id'))-1] = request.POST.get('answer')
    user.profile.testAnswers = json.dumps(testAnswers)
    user.profile.save()
    return HttpResponse()

def submit_practice_test(request, topic, answers):
    if not request.user.is_authenticated:
        return render(request, 'core/login.html', {"gotLoggedOut": True})
    user = request.user
    testTime = json.loads(user.profile.testTime)
    testTime[topic] = "-1"
    user.profile.testTime = json.dumps(testTime)

    currQuestions = json.loads(user.profile.testQuestion)
    questions = [get_object_or_404(Question, pk=currQuestions[topic][i]) for i in range(5)]

    numCorrect = 0
    distribution = []
    for i in range(len(questions)):
        if answers[i].replace(" ", "") in questions[i].answer.replace(" ", "").split("@"):
            numCorrect += 1
            distribution.append(1)
        else:
            distribution.append(0)

    testProgress = json.loads(user.profile.testProgress)
    testProgress[topic] = numCorrect
    user.profile.testProgress = json.dumps(testProgress)
    testDistribution = json.loads(user.profile.testDistribution)
    testDistribution[topic] = distribution
    user.profile.testDistribution = json.dumps(testDistribution)
    user.profile.save()

    if (request.is_ajax()):
        return "You scored "+str(numCorrect)+"/5 correct"

    return practice_tests_detail(request, topic[5:])

def update_profiles(request):
    user = User.objects.create_user('toDelete', 'andrewmilas10@gmail.com', 'letitbe1')
    otherProfiles = Profile.objects.all()
    profile = Profile.objects.create(user=user)

    def newD(old, newKey, newValue):
        old[newKey] = newValue
        return old

    for prof in otherProfiles:
        progress2 = json.loads(profile.progress2)
        for topic in progress2.keys():
            # print(topic)
            if topic not in json.loads(prof.progress2).keys():
                prof.progress2 = json.dumps(newD(json.loads(prof.progress2), topic, json.loads(profile.progress2)[topic]))
                prof.currQuestions = json.dumps(newD(json.loads(prof.currQuestions), topic, json.loads(profile.currQuestions)[topic]))
                prof.attempts = json.dumps(newD(json.loads(prof.attempts), topic, json.loads(profile.attempts)[topic]))
                prof.currCorrect = json.dumps(newD(json.loads(prof.currCorrect), topic, json.loads(profile.currCorrect)[topic]))
                prof.topicOrder = json.dumps(newD(json.loads(prof.topicOrder), topic, json.loads(profile.topicOrder)[topic]))
                prof.currAnswer = json.dumps(newD(json.loads(prof.currAnswer), topic, json.loads(profile.currAnswer)[topic]))
                prof.save()
        testProgress = json.loads(profile.testProgress)
        for topic in testProgress.keys():
            print(topic)
            if topic not in json.loads(prof.testProgress).keys():
                prof.testProgress = json.dumps(newD(json.loads(prof.testProgress), topic, json.loads(profile.testProgress)[topic]))
                prof.testTime = json.dumps(newD(json.loads(prof.testTime), topic, json.loads(profile.testTime)[topic]))
                prof.testQuestion = json.dumps(newD(json.loads(prof.testQuestion), topic, json.loads(profile.testQuestion)[topic]))
                prof.testAnswers = json.dumps(newD(json.loads(prof.testAnswers), topic, json.loads(profile.testAnswers)[topic]))
                prof.testDistribution = json.dumps(newD(json.loads(prof.testDistribution), topic, json.loads(profile.testDistribution)[topic]))
                prof.save()

    # user = authenticate(username=username, password=password)
    profile.delete()
    user.delete()
    return HttpResponse()

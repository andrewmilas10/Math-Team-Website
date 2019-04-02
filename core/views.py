from django.shortcuts import render, get_object_or_404
from .models import Post
from .models import Question
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm
from django.http import JsonResponse
from django.db.models import Q


def index(request):
    return render(request, 'core/index.html', {})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'core/post_list.html', {'posts': posts})

#this is the function that is loaded when the list of questions is called, it also works on the search functionality of the
#website by finding the questions under the filter with a serach query
def question_list(request):
    topiclist = ['Ratios, Proportions and Percents','Number Theory and Divisibility','Counting Basics and Probability'
    , 'Quadratics', 'Probability', 'Advanced Geometrical Concepts', 'Perimeter, Area and Surface Area',
    'Logic, Sets and Venn Diagram', 'Similarity', 'Coordiante Geometry', 'Circles', 'Trigonometry',
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
            return render(request, 'core/questions.html', {
                        'questions': questions,
                        'question_results': question_results,
                    })


        return render(request, 'core/question_list.html', {'questions': questions})



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
        'question': question
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
        }
        return render(request, 'core/question_detail.html', context)
    else:
        return render(request, 'core/question_detail.html', {'question': question})


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

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'core/homepage_logged_in.html', {})
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
                return render(request, 'core/homepage_logged_in.html', {'questions': questions})
            else:
                return render(request, 'core/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'core/login.html', {'error_message': 'Invalid login'})
    return render(request, 'core/login.html')

def homepage(request):
    return render(request, 'core/homepage_logged_in.html', {})

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
        })

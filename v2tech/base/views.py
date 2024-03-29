# from urllib import request
from audioop import reverse
from pydoc import pager
from pydoc_data.topics import topics
import re
from unicodedata import name
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect 
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from pickle import GET
from django.db.models import Q
from .models import Profile, Question, Topic, User, Answer
from .forms import QuestionForm,ProfileUpdateForm, UserUpdateForm, AnswerForm,UserRegisterForm
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist!')

    context = {'page':page}
    return render(request, 'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()
            messages.success(request, f'Account Successfully created for {username}! Login In Now')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'base/login_register.html', {'form': form})



@login_required(login_url='/login')
def profilePage(request, pk):
    user_profile =Profile.objects.get(user=request.user)
    user = User.objects.get(id=pk)
    questions = user.question_set.all()
    context = {'user':user, 'questions':questions, 'user_profile':user_profile}
    return render(request,'base/profile.html', context)



@login_required(login_url='/login')
def profilePageUpdate(request):
    user_profile =Profile.objects.get(user=request.user)
    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.image
            bio = request.POST['bio']
            phone = request.POST['phone']

            user_profile.image = image
            user_profile.bio = bio
            user_profile.phone = phone
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            phone = request.POST['phone']

            user_profile.image = image
            user_profile.bio = bio
            user_profile.phone = phone
            user_profile.save()

        return redirect(f'profile/{user_profile.id_user}')


    return render(request, 'base/profile_update.html', {'user_profile': user_profile})


def questionList(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    questions = Question.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
        )
    topics = Topic.objects.all()[0:3]
    questions_count = questions.count()
    context =  {'questions':questions, 'topics':topics,'questions_count':questions_count}
    return render(request, 'base/question_list.html',context)

#home page
def home(request):
    users = Profile.objects.all()
    users_count = users.count()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    questions = Question.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
        # Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    # questions_count = questions.count()
    context =  {'questions':questions, 'topics':topics,'users_count':users_count}
    return render(request,'base/home.html',context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    question = user.question_set.all()
    question_answer = user.answer_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'question': question,
               'question_answer': question_answer, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserUpdateForm(instance=user)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

#Question Creation page
def question(request,pk):
    question = Question.objects.get(id=pk)
    answers = question.answer_set.all().order_by('-created')
    participants = question.participants.all()

    if request.method == 'POST':
        answer = Answer.objects.create(
            user = request.user,
            question = question,
            body = request.POST.get('body')
        )
        question.participants.add(request.user)
        return redirect('question',pk=question.id)

    context =  {'question':question, 'answers':answers, 'participants':participants}
    return render(request,'base/question_detail.html',context)

@login_required(login_url='/login')
def createQuestion(request):
    form = QuestionForm()
    topics = Topic.objects.all()
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Question.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('questionlist')
    context = {'form':form,'topics': topics}
    return render(request, 'base/question_form.html', context)


@login_required(login_url='/login')
def updateQuestion(request, pk):
    question = Question.objects.get(id=pk)
    form = QuestionForm(instance=question)
    topics = Topic.objects.all()

    if request.user != question.host:
        return HttpResponse("Your not allowed here")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        question.topic=topic
        question.name=request.POST.get('name')
        question.description=request.POST.get('description')
        question.save()

        return redirect('questionlist')

    context = {'form':form,'topics': topics,'question':question}
    return render(request,'base/question_form.html',context)

@login_required(login_url='/login')
def deleteQuestion(request, pk):
    obj = Question.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('questionlist')
    return render(request,'base/delete.html', {'obj':obj})


@login_required(login_url='/login')
def deleteAnswer(request, pk):
    answer = Answer.objects.get(id=pk)

    if request.user != answer.user:
        return HttpResponse("Your not allowed here")

    if request.method == 'POST':
        answer.delete()
        return redirect('questionlist')
    return render(request,'base/delete.html', {'obj':answer})


# def like_view(request, pk):
#     post = get_object_or_404(Question, id=request.POST.get('answer_id'))
#     liked = False
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#         liked = False
#     else:
#         post.likes.add(request.user)
#         liked = True
#     return HttpResponseRedirect(reverse('question-detail', args=[str(pk)]))
def Like_post(request):
    user = request.user
    if request.method == 'POST': 
        post_id= request.POST.get('post_id') 
        post_obj = Answer.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.Liked.remove(user) 
        else:
            post_obj.liked.add(user)
            
        like, created = Like.objects.get_or_create(user=user, post_id=post_id)
        
        if not created:
            if like.value=='Like':
                like.value = 'Unlike'
            else:
                like.value="Like"
                
        like.save()

    return redirect('questionlist')


def AddAnswer(request,pk):
    question = Question.objects.get(id=pk)
    answers = question.answer_set.all().order_by('-created')
    participants = question.participants.all()
    form = AnswerForm()
    if request.method == 'POST':
        answer = Answer.objects.create(
            user = request.user,
            question = question,
            body = request.POST.get('body')
        )
        question.participants.add(request.user)
        return redirect('question',pk=question.id)

    context =  {'form':form, 'question':question, 'answers':answers, 'participants':participants}
    return render(request,'base/question-answer.html',context)
    
def TopicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request,'base/topic.html',{'topics':topics})

    
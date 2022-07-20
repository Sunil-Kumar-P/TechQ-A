# from urllib import request
from pydoc import pager
import re
from django.shortcuts import render, redirect 
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from pickle import GET
from django.db.models import Q
from .models import Question, Topic, User, Answer
from .forms import QuestionForm,ProfileUpdateForm, UserUpdateForm


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
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An Error occured whlie user registration!')

    return render(request,'base/login_register.html', {'form':form})

@login_required(login_url='/login')
def profilePage(request):
    
    return render(request,'base/profile.html')

@login_required(login_url='/login')
def profilePageUpdate(request):
    # form = ProfileForm
    # if request.method == 'POST':
    #     form = ProfileForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('profile')
    # context = {'form':form}
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Acount Updated Successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request,'base/profile_update.html', context)

#home page
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    questions = Question.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    questions_count = questions.count()
    context =  {'questions':questions, 'topics':topics,'questions_count':questions_count}
    return render(request,'base/home.html',context)

def questionList(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    questions = Question.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    questions_count = questions.count()
    context =  {'questions':questions, 'topics':topics,'questions_count':questions_count}
    return render(request, 'base/question_list.html',context)

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
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/question_form.html', context)

@login_required(login_url='/login')
def updateQuestion(request, pk):
    question = Question.objects.get(id=pk)
    form = QuestionForm(instance=question)

    if request.user != question.host:
        return HttpResponse("Your not allowed here")

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'base/question_form.html',context)

@login_required(login_url='/login')
def deleteQuestion(request, pk):
    obj = Question.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    return render(request,'base/delete.html', {'obj':obj})


@login_required(login_url='/login')
def deleteAnswer(request, pk):
    answer = Answer.objects.get(id=pk)

    if request.user != answer.user:
        return HttpResponse("Your not allowed here")

    if request.method == 'POST':
        answer.delete()
        return redirect('home')
    return render(request,'base/delete.html', {'obj':answer})
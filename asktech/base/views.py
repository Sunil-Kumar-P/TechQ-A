import email

from urllib import request
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from pickle import GET
from django.db.models import Q
from .models import Question, Topic, User
from .forms import QuestionForm


def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist!')

    context = { }
    return render(request, 'base/login_register.html',context)

def logoutUser(resquest):
    logout(request)
    return redirect('home')

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

#room page
def question(request,pk):
    questions = Question.objects.get(id=pk)
    context =  {'questions':questions}
    return render(request,'base/question.html',context)

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
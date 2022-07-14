from pickle import GET
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Question, Topic
from .forms import QuestionForm



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


def createQuestion(request):
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/question_form.html', context)

def updateQuestion(request, pk):
    question = Question.objects.get(id=pk)
    form = QuestionForm(instance=question)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'base/question_form.html',context)


def deleteQuestion(request, pk):
    obj = Question.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    return render(request,'base/delete.html', {'obj':obj})
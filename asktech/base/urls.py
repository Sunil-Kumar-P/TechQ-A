from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('question/<str:pk>/', views.question, name="question"),
    path('create-question/',views.createQuestion, name="create-question"),
    path('update-question/<str:pk>/',views.updateQuestion, name="update-question"),
    path('delete-question/<str:pk>/',views.deleteQuestion, name="delete-question"),
]

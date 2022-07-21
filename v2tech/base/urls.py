from django.urls import path

from . import views

urlpatterns = [
    path('login/',views.loginPage, name="login"),
    path('logout/',views.logoutUser, name="logout"),
    path('register/',views.registerUser, name="register"),
    
    path('',views.home, name="home"),
    path('question-list',views.questionList, name="question-list"),
    path('profile/<str:pk>',views.profilePage, name="profile"),
    path('profile-update',views.profilePageUpdate, name="profile-update"),
    path('question/<str:pk>/', views.question, name="question"),
    path('create-question/',views.createQuestion, name="create-question"),
    path('update-question/<str:pk>/',views.updateQuestion, name="update-question"),
    path('delete-question/<str:pk>/',views.deleteQuestion, name="delete-question"),
    path('delete-answer/<str:pk>/',views.deleteAnswer, name="delete-answer"),
]

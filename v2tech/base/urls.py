from django.urls import path

from . import views

urlpatterns = [
    path('login/',views.loginPage, name="login"),
    path('logout/',views.logoutUser, name="logout"),
    path('register/',views.registerUser, name="register"),
    
    path('',views.home, name="questionlist"),
    path('home',views.questionList, name="home"),
    path('profile/<str:pk>',views.profilePage, name="profile"),
    path('profile-update',views.profilePageUpdate, name="profile-update"),
    path('question/<str:pk>/', views.question, name="question"),
    path('create-question/',views.createQuestion, name="create-question"),
    path('update-question/<str:pk>/',views.updateQuestion, name="update-question"),
    path('delete-question/<str:pk>/',views.deleteQuestion, name="delete-question"),
    path('question/<int:pk>/comment/', views.AddAnswerView.as_view(), name="question-answer"),
    path('delete-answer/<str:pk>/',views.deleteAnswer, name="delete-answer"),
    path('like/<int:pk>', views.like_view, name="like_post")
]

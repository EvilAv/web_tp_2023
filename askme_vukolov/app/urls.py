from django.contrib import admin
from django.urls import path, include

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('question/<int:id>', views.detail_question, name='detail_question'),
    path('tag/<str:slag>', views.questions_by_tag, name='tag'),
    path('login', views.login, name='login'),
]

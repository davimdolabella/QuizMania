
from django.urls import path
from . import views
app_name = 'quizmania'
urlpatterns = [
    path('', views.home, name='home'),
]

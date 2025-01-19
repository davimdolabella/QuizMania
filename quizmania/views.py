from django.shortcuts import render

def home(request):
    return render(request, 'quizmania/pages/home.html')
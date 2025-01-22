from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . import models

class QuizListViewBase(ListView):
    model = models.Quiz
    context_object_name = 'quizes'
    ordering = ['?']
    template_name = ''
    paginate_by = None

class HomeQuizListViewBase(QuizListViewBase):
    template_name = 'quizmania/pages/home.html'
    
class QuizDetail(DetailView):
    model = models.Quiz
    context_object_name = 'quiz'
    template_name = 'quizmania/pages/quiz_detail.html'
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        quiz = ctx.get('quiz')
        ctx.update({
            'title':quiz.questions.all().first().answers.all().order_by('?'),
        })
        return ctx
    

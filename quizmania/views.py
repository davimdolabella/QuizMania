from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . import models

class QuizListViewBase(ListView):
    model = models.Quiz
    context_object_name = 'quizes'
    ordering = ['difficulty']
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
            'easy_questions':len(quiz.questions.all().filter(difficulty__pk=1)),
            'mid_questions':len(quiz.questions.all().filter(difficulty__pk=2)),
            'diff_questions':len(quiz.questions.all().filter(difficulty__pk=3)),
        })
        return ctx
    

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
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
    template_name = 'quizmania/pages/quiz.html'
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        quiz = ctx.get('quiz')
        questions_id =[question.id for question in quiz.questions.all().order_by('?')] 
        question_id = questions_id[0]
        self.request.session['current_quiz_questions_id'] = questions_id
        print(self.request.session['current_quiz_questions_id'], question_id) 
        ctx.update({
            'easy_questions':len(quiz.questions.all().filter(difficulty__pk=1)),
            'mid_questions':len(quiz.questions.all().filter(difficulty__pk=2)),
            'diff_questions':len(quiz.questions.all().filter(difficulty__pk=3)),
            'question_id': question_id
        })
        return ctx

class QuizCurrentQuestion(DetailView):
    model = models.Question
    context_object_name = 'question'
    template_name = 'quizmania/pages/quiz.html'
    def get(self, request, *args, **kwargs):
        questions_id = self.request.session.get('current_quiz_questions_id', [])
        questions_id.pop(0)
        next_question_id = questions_id[0] if questions_id else None
        self.request.session['current_quiz_questions_id'] = questions_id
        self.request.session['next_question_id'] = next_question_id

        if not questions_id and questions_id != []:
            return redirect(reverse('quizmania:home'))
        
        return super().get(request, *args, **kwargs)
    

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        question = ctx.get('question')
        
        print(self.request.session['current_quiz_questions_id']) 
        ctx.update({
            'answers': question.answers.all().order_by('?'),
            'question_img': question.quiz.cover.url
        })

        return ctx
class Is_Correct(View):
    def get(self, request, pk):
        
        answer = models.Answer.objects.filter(pk=pk).first()
        is_correct = answer.is_correct
        next_question_id = self.request.session.get('next_question_id', [])
        return render(request, 'quizmania/pages/quiz.html',{
            'is_correct_page':True,
            'is_correct_answer': is_correct,
            'correct_answer': answer.question.answers.all().filter(is_correct=True).first(),
            'next_question_id': next_question_id
        })
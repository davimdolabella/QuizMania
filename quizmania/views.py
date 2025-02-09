from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from . import models
LOGIN_URL = 'authors:login'
REDIRECT_FIELD_NAME = 'next'

def get_quiz_session(request, quiz):
    user = request.user 
    session, created = models.QuizSession.objects.get_or_create(
        user=user,
    )
    session.current_quiz = quiz
    session.save()
    return session
def get_user_profile(request):
    user = request.user 
    profile, created = models.Profile.objects.get_or_create(user=user)
    return profile
def save_in_profile(profile, quiz_session):
    profile.completed_quizes.add(quiz_session.current_quiz)
    profile.correct_questions += quiz_session.correct_answers
    profile.incorrect_questions += quiz_session.incorrect_answers
    profile.points += quiz_session.points
    profile.correct_questions_percentage = profile.calculate_correct_questions_percentage()
    profile.incorrect_questions_percentage = 100 - profile.correct_questions_percentage
    profile.ranking = profile.get_rank_position()
    profile.save()

class QuizListViewBase(ListView):
    model = models.Quiz
    context_object_name = 'quizes'
    ordering = ['category','difficulty']
    template_name = ''
    paginate_by = None
    

class HomeQuizListViewBase(QuizListViewBase):
    template_name = 'quizmania/pages/home.html'
    

class QuizDetail(DetailView):
    model = models.Quiz
    context_object_name = 'quiz'
    template_name = 'quizmania/pages/quiz.html'
    
    def get_questions_by_difficulty(self, quiz, difficulty_id, limit):
        if not limit:
            return []
        else:
            return list([question.id for question in quiz.category.questions.all().filter(difficulty__id=difficulty_id).order_by('?')][:(limit)])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        quiz = context.get('quiz')
        questions_id =[] 
        questions_id.extend(
            self.get_questions_by_difficulty(quiz, difficulty_id=1, limit=quiz.qnt_easy_questions) +
            self.get_questions_by_difficulty(quiz, difficulty_id=2, limit=quiz.qnt_mid_questions) +
            self.get_questions_by_difficulty(quiz, difficulty_id=3, limit=quiz.qnt_diff_questions)
        )
        question_id = questions_id[0]
        if self.request.user.is_authenticated:
            quiz_session = get_quiz_session(self.request, quiz)
            quiz_session.reset_session()
            quiz_session.questions_list = questions_id
            quiz_session.current_question = question_id
            quiz_session.save()

        context.update({
            'easy_questions':quiz.qnt_easy_questions,
            'mid_questions':quiz.qnt_mid_questions,
            'diff_questions':quiz.qnt_diff_questions,
            'question_id': question_id
        })
        return context

class QuizCurrentQuestion(DetailView):
    model = models.Question
    context_object_name = 'question'
    template_name = 'quizmania/pages/quiz.html'
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.info(self.request, "Entre em sua conta para jogar...")
            return redirect(reverse('authors:login'))
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, *args, **kwargs):
        session_quiz = get_object_or_404(models.QuizSession, user=self.request.user)
        cover_url = session_quiz.current_quiz.cover.url
        context = super().get_context_data(*args, **kwargs)
        question = context.get('question')
        context.update({
            'answers': question.answers.all().order_by('?'),
            'question_img': cover_url,
            'is_in_a_quiz':True,
        })

        return context
    
class Is_Correct(LoginRequiredMixin, View):
    login_url = LOGIN_URL
    redirect_field_name = REDIRECT_FIELD_NAME
    def post(self, request, pk):
        quiz_session = get_object_or_404(models.QuizSession, user=request.user)
        questions_id = quiz_session.questions_list
        if not questions_id:
            return redirect(reverse('quizmania:home'))
        questions_id.pop(0)
        answer = get_object_or_404(models.Answer, pk=pk)
        is_correct = answer.is_correct
        quiz_session.questions_list = questions_id
        answers = quiz_session.answers if quiz_session.answers else []
        answers.append({'is_correct':is_correct, 'difficulty':answer.question.difficulty.name})
        quiz_session.answers = answers
        quiz_session.save()
        return redirect(reverse('quizmania:is_correct', kwargs={'pk': pk}))
    
    def get(self, request, pk):
        quiz_session = get_object_or_404(models.QuizSession, user=request.user)
        answer = get_object_or_404(models.Answer, pk=pk)
        is_correct = answer.is_correct
        next_question_id = quiz_session.questions_list[0] if quiz_session.questions_list else None
        return render(request, 'quizmania/pages/quiz.html',{
            'is_correct_page':True,
            'is_correct_answer': is_correct,
            'correct_answer': answer.question.answers.all().filter(is_correct=True).first(),
            'next_question_id': next_question_id,
            'is_in_a_quiz':True,
        })
    
class Show_Result(LoginRequiredMixin, View):
    login_url = LOGIN_URL
    redirect_field_name = REDIRECT_FIELD_NAME
    def post(self, request):
        quiz_session = get_object_or_404(models.QuizSession, user=request.user)
        quiz_session.get_points()
        quiz_session.calculate_correct_answers_percentage()
        profile = get_user_profile(request)
        save_in_profile(profile, quiz_session)
        return redirect(reverse('quizmania:show_result'))
    def get(self, request):
        quiz_session = get_object_or_404(models.QuizSession, user=request.user)
        quiz_points = quiz_session.points
        correct_answers_percentage = quiz_session.correct_answers_percentage
        is_a_good_result = quiz_session.is_a_good_result
        return render(request, 'quizmania/pages/quiz.html',{
            'is_result_page':True,
            'quiz_points':quiz_points,
            'correct_answers': f'{correct_answers_percentage:.0f}%',
            'incorrect_answers':f'{100 - correct_answers_percentage:.0f}%',
            'is_a_good_result':is_a_good_result,
            'is_in_a_quiz':True,
        })
    
class UserProfile(LoginRequiredMixin, DetailView):
    model = models.User
    context_object_name = 'user'
    template_name = 'quizmania/pages/profile.html'
    login_url = LOGIN_URL
    redirect_field_name = REDIRECT_FIELD_NAME
    def get_object(self, queryset = None):
        return self.request.user

class Ranking(ListView):
    model = models.Profile
    context_object_name = 'profiles'
    template_name = 'quizmania/pages/ranking.html'
    def get_object(self, queryset = None):
        return self.request.user.profile
    def get_queryset(self):
        return models.Profile.objects.all().order_by('-points')
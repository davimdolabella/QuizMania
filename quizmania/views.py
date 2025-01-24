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
        self.request.session.flush()
        ctx = super().get_context_data(*args, **kwargs)
        quiz = ctx.get('quiz')
        questions_id =[] 
        
        if quiz.qnt_easy_questions:
            questions_id.extend([question.id for question in quiz.category.questions.all().filter(difficulty__id=1).order_by('?')][:(quiz.qnt_easy_questions)])
        if quiz.qnt_mid_questions:
            questions_id.extend([question.id for question in quiz.category.questions.all().filter(difficulty__id=2).order_by('?')][:(quiz.qnt_mid_questions)])
        if quiz.qnt_diff_questions:
            questions_id.extend([question.id for question in quiz.category.questions.all().filter(difficulty__id=3).order_by('?')][:(quiz.qnt_diff_questions)])

        question_id = questions_id[0]
        print(questions_id)
        self.request.session['current_quiz_cover_url'] = quiz.cover.url
        self.request.session['current_quiz_questions_id'] = questions_id
        ctx.update({
            'easy_questions':quiz.qnt_easy_questions,
            'mid_questions':quiz.qnt_mid_questions,
            'diff_questions':quiz.qnt_diff_questions,
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
        cover_url = self.request.session.get('current_quiz_cover_url')
        ctx = super().get_context_data(*args, **kwargs)
        question = ctx.get('question')
        ctx.update({
            'answers': question.answers.all().order_by('?'),
            'question_img': cover_url
        })

        return ctx
    
class Is_Correct(View):
    def get(self, request, pk):
        answers = self.request.session.get('answers_current_quiz',[])
        answer = models.Answer.objects.filter(pk=pk).first()
        is_correct = answer.is_correct
        answers.append([is_correct,str(answer.question.difficulty) ])
        
        self.request.session['answers_current_quiz'] = answers
        next_question_id = self.request.session.get('next_question_id', [])
        


        return render(request, 'quizmania/pages/quiz.html',{
            'is_correct_page':True,
            'is_correct_answer': is_correct,
            'correct_answer': answer.question.answers.all().filter(is_correct=True).first(),
            'next_question_id': next_question_id
        })
    
class Show_Result(View):
    def get(self, request):
         
        answers = self.request.session.get('answers_current_quiz',[])
        correct_answers = 0
        incorrect_answers = 0
        quiz_points = 0
        is_a_good_result = False

        for list in answers:
            if list[0]:
                correct_answers += 1
                if 'D' in list[1]:
                    quiz_points += 3
                elif 'M' in list[1]:
                    quiz_points +=2
                elif 'F' in list[1]:
                    quiz_points += 1
            else:
                incorrect_answers += 1
        x = 100/ (correct_answers + incorrect_answers)
        correct_answers_percentage = x * correct_answers
        incorrect_answers_percentage = x * incorrect_answers
        if correct_answers * x > 60:
            is_a_good_result = True
        return render(request, 'quizmania/pages/quiz.html',{
            'is_result_page':True,
            'quiz_points':quiz_points,
            'correct_answers': f'{correct_answers_percentage:.0f}%',
            'incorrect_answers':f'{incorrect_answers_percentage:.0f}%',
            'is_a_good_result':is_a_good_result,
        })
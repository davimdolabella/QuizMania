from django.db import models
from django.contrib.auth.models import User
import math

class Category(models.Model):
    name = models.CharField(max_length=65)
    def __str__(self):
        return self.name

class Difficulty(models.Model):
    name = models.CharField(max_length=65)
    def __str__(self):
        return self.name

class Quiz(models.Model):
    def __str__(self):
        return f"{self.title}({self.category})"
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover = models.ImageField(upload_to='quiz/covers/%Y/%m/%d/', blank=True, null=True)
    qnt_easy_questions = models.IntegerField(null=True, blank=True)
    qnt_mid_questions = models.IntegerField(null=True, blank=True)
    qnt_diff_questions = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='quizes', null=True
    )
    difficulty = models.ForeignKey(
        Difficulty, on_delete=models.SET_NULL, null=True, 
    )

    

class Question(models.Model):
    def __str__(self):
        return self.question

    question = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    difficulty = models.ForeignKey(
        Difficulty, on_delete=models.CASCADE, related_name='questions' 
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='questions', null=True
    )

class Answer(models.Model):
    def __str__(self):
        return self.answer
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers'
    )    

class Profile(models.Model):
    def __str__(self):
        return f'profile of {self.user}'
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    completed_quizes = models.ManyToManyField(
        Quiz, blank=True, related_name='profiles'
    )
    correct_questions = models.IntegerField(default=0)
    incorrect_questions = models.IntegerField(default=0)
    correct_questions_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,  
        default=0.00 
    )
    points = models.IntegerField(default=0)
    ranking = models.PositiveIntegerField(blank=True, null=True)
    def calculate_correct_questions_percentage(self):
        total_questions = self.correct_questions + self.incorrect_questions
        if total_questions > 0:
            self.save()
            return (self.correct_questions * 100) / total_questions
        return 0.00

    def get_rank_position(self):
        all_profiles = Profile.objects.all().order_by('-points')
        profile_position = 0
        for index, profile in enumerate(all_profiles):
            if profile == self:
                profile_position= index + 1
            profile.ranking = index + 1  
            profile.save()
        return profile_position if profile_position > 0 else None

    

class QuizSession(models.Model):
    def __str__(self):
        return f'session of {self.user}'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    current_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True, null=True)
    current_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    questions_list = models.JSONField(default=list, blank=True)
    answers = models.JSONField(default=list, blank=True)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lifes = models.IntegerField(default=0, blank=True)
    correct_answers = models.IntegerField(default=0, blank=True)
    incorrect_answers = models.IntegerField(default=0, blank=True)
    correct_answers_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,  
        default=0.00 
    )
    # model of answer in list answers is [{"is_correct":True, "difficulty":'Difícil'},{"is_correct":True, "difficulty":'Fácil'}, ...]
    def get_points(self):
        self.points = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        for answer in self.answers:
            is_correct = answer.get("is_correct", False)
            difficulty = answer.get("difficulty", "")
            if is_correct:
                self.correct_answers += 1
                if difficulty == "Difícil":
                    self.points += 3
                elif difficulty == "Médio":
                    self.points += 2
                elif difficulty == "Fácil":
                    self.points += 1
            else:
                self.incorrect_answers += 1

        self.save()
    @property
    def is_a_good_result(self):
        return self.correct_answers_percentage > 60

    def calculate_correct_answers_percentage(self):
        total_answers = self.correct_answers + self.incorrect_answers
        self.correct_answers_percentage =  (self.correct_answers * 100) / total_answers
        self.save()

    def reset_session(self):
        self.questions_list = []
        self.answers = []
        self.points = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.correct_answers_percentage = 0.00
        self.current_question = None
        self.save()

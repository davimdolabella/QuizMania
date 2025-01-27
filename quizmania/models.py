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
    
    points = models.IntegerField(default=0)
    ranking = models.PositiveIntegerField(blank=True, null=True)
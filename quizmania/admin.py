from django.contrib import admin
from . import models
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    ...
@admin.register(models.Difficulty)
class DifficultyAdmin(admin.ModelAdmin):
    ...
    
@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    ...
    
@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    ordering=['id']
    list_display = [ 'question', 'difficulty', 'category']

    
@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer','question', 'is_correct']
     
@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    ordering=['-points','ranking']
    list_display = ['user','correct_questions','points', 'ranking']

@admin.register(models.QuizSession)
class QuizSession(admin.ModelAdmin):
    ...
     

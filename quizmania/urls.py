
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'quizmania'
urlpatterns = [
    path('', views.HomeQuizListViewBase.as_view(), name='home'),
    path('quiz/<int:pk>', views.QuizDetail.as_view(), name='quiz'),
    path('quiz/question/<int:pk>', views.QuizCurrentQuestion.as_view(), name='question'),
    path('quiz/question/is_correct/<int:pk>', views.Is_Correct.as_view(), name='is_correct'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

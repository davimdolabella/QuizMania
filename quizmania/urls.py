
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'quizmania'
urlpatterns = [
    path('', views.HomeQuizListViewBase.as_view(), name='home'),
    path('quiz/<int:pk>', views.QuizDetail.as_view(), name='quiz'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

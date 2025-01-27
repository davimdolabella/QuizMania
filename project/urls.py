
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quizmania.urls')),
    path('authors/', include('authors.urls')),
]

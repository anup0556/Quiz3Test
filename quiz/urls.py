from django.contrib import admin
from django.urls import path
from questions.views import QuestionList, SubmitAnswer, Leaderboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/questions/', QuestionList.as_view(), name='question-list'),
    path('api/submit-answer/', SubmitAnswer.as_view(), name='submit-answer'),
    path('api/leaderboard/', Leaderboard.as_view(), name='leaderboard'),
]
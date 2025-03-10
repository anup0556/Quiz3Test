from django.contrib import admin
from django.urls import path
from users.views import UserRegistrationView
from questions.views import QuestionList, SubmitAnswer, QuestionDetail, Leaderboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/questions/', QuestionList.as_view(), name='question-list'),
    path('api/questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('api/submit-answer/', SubmitAnswer.as_view(), name='submit-answer'),
    path('api/leaderboard/', Leaderboard.as_view(), name='leaderboard'),
]

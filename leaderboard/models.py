from django.db import models
from django.contrib.auth.models import User

class LeaderBoard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions_attempted = models.IntegerField(default=0)
    last_played = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"{self.user.username} - Score: {self.score}"

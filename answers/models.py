from django.db import models
from django.contrib.auth.models import User
from questions.models import Question

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This ensures one user can attempt one question only once
        unique_together = ['user', 'question']

    def save(self, *args, **kwargs):
        # Direct comparison with question's correct answer
        self.is_correct = self.selected_answer == self.question.correct_answer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.question.question_text[:30]}"

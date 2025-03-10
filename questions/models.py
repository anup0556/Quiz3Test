from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    options = models.JSONField(default=dict)
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

class QuestionAttempt(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_ip = models.CharField(max_length=45, db_index=True)
    selected_answer = models.CharField(max_length=200)
    is_correct = models.BooleanField(db_index=True)
    attempted_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_ip', 'is_correct']),
            models.Index(fields=['-attempted_at']),
        ]
        unique_together = ['question', 'user_ip']

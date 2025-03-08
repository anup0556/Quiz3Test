from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    options = models.JSONField(default=dict)
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

class QuestionAttempt(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_ip = models.CharField(max_length=45)
    selected_answer = models.CharField(max_length=200)
    is_correct = models.BooleanField()
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['question', 'user_ip']

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LeaderBoard
from answers.models import Answer
from questions.models import Question
from django.db.models import Count, F
from django.utils.timezone import now

class LeaderboardView(APIView):
    def get(self, request):
        current_time = now()  # This will include nanoseconds
        total_questions = Question.objects.count()
        
        # Get all users sorted by total points from correct answers
        leaderboard = LeaderBoard.objects.annotate(
            total_points=Count('user__answer', filter=F('user__answer__is_correct'), distinct=True) * 10
        ).order_by('-total_points', '-score')
        
        rankings = []
        for rank, entry in enumerate(leaderboard, 1):
            user_answers = Answer.objects.filter(user=entry.user)
            correct_answers = user_answers.filter(is_correct=True).count()
            incorrect_answers = user_answers.filter(is_correct=False).count()
            total_points = correct_answers * 10
            
            rankings.append({
                'rank': rank,
                'username': entry.user.username,
                'quiz_progress': {
                    'total_questions': total_questions,
                    'attempted': user_answers.count(),
                    'remaining': total_questions - user_answers.count()
                },
                'performance': {
                    'correct_answers': correct_answers,
                    'incorrect_answers': incorrect_answers,
                    'accuracy': f"{(correct_answers / user_answers.count() * 100) if user_answers.count() > 0 else 0:.1f}%"
                },
                'points': {
                    'total_points': total_points,
                    'points_per_correct': 10,
                    'total_possible_points': total_questions * 10
                }
            })
        
        return Response({
            'status': 'success',
            'leaderboard': rankings
        })

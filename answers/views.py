from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Answer
from questions.models import Question
from django.contrib.auth.models import User
from django.utils import timezone
from leaderboard.models import LeaderBoard

class SubmitAnswerView(APIView):
    def post(self, request):
        user_id = request.data.get('user')
        question_id = request.data.get('question')
        selected_answer = request.data.get('selected_answer')  # Add this line

        # Check if already attempted
        if Answer.objects.filter(user_id=user_id, question_id=question_id).exists():
            return Response({
                'status': 'error',
                'message': 'You have already attempted this question. Please try a different question.'
            })
        
        try:
            user = User.objects.get(id=user_id)
            question = Question.objects.get(id=question_id)
            
            # Check if answer is correct
            is_correct = selected_answer == question.correct_answer
            
            # Create answer
            answer = Answer.objects.create(
                user=user,
                question=question,
                selected_answer=selected_answer,
                is_correct=is_correct
            )

            # Update or create leaderboard entry
            leaderboard_entry, created = LeaderBoard.objects.get_or_create(user=user)
            leaderboard_entry.total_questions_attempted += 1
            
            # Update score: +10 for correct, 0 for incorrect
            if is_correct:
                leaderboard_entry.score += 10
            # No points deduction for incorrect answers
            
            leaderboard_entry.save()

            return Response({
                'status': 'success',
                'message': 'Answer submitted successfully',
                'is_correct': is_correct,
                'points': '+10' if is_correct else '0',  # Updated to show 0 points for incorrect
                'current_score': leaderboard_entry.score
            })

        except (User.DoesNotExist, Question.DoesNotExist):
            return Response({
                'status': 'error',
                'message': 'Invalid user or question ID'
            })

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question, QuestionAttempt
from django.db.models import Count, F, Q, FloatField, Avg, Max  # Added Max here
from django.db.models.functions import Cast
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class QuestionList(APIView):
    def get(self, request):
        questions = Question.objects.all()
        questions_data = [{
            'id': q.id,
            'question_text': q.question_text,
            'options': q.options
        } for q in questions]
        return Response({
            "status": "success",
            "questions": questions_data
        })

class SubmitAnswer(APIView):
    def post(self, request):
        try:
            question_id = request.data.get('question_id')
            selected_answer = request.data.get('selected_answer')
            user_ip = self.get_client_ip(request)

            if not question_id or not selected_answer:
                return Response({
                    "status": "error",
                    "message": "Both question_id and selected_answer are required"
                }, status=status.HTTP_400_BAD_REQUEST)

            question = Question.objects.get(id=question_id)

            # Check if already attempted
            if QuestionAttempt.objects.filter(question=question, user_ip=user_ip).exists():
                return Response({
                    "status": "error",
                    "message": "You have already attempted this question"
                }, status=status.HTTP_400_BAD_REQUEST)

            is_correct = question.correct_answer == selected_answer

            # Save the attempt
            QuestionAttempt.objects.create(
                question=question,
                user_ip=user_ip,
                selected_answer=selected_answer,
                is_correct=is_correct
            )

            # After saving the attempt, broadcast the update
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "quiz_room",
                {
                    "type": "quiz_update",
                    "message": {
                        "type": "answer_submitted",
                        "user_ip": user_ip,
                        "is_correct": is_correct
                    }
                }
            )

            return Response({
                "status": "success",
                "is_correct": is_correct,
                "message": "Correct answer!" if is_correct else "Wrong answer!"
            })

        except Question.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Question not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class Leaderboard(APIView):
    def get(self, request):
        try:
            leaderboard_data = QuestionAttempt.objects.values(
                'user_ip'
            ).annotate(
                total_attempts=Count('id'),
                correct_answers=Count('id', filter=Q(is_correct=True)),
                accuracy=Cast(F('correct_answers') * 100.0 / F('total_attempts'), FloatField()),
                score=F('correct_answers') * 10,
                last_attempt=Max('attempted_at')
            ).order_by(
                '-score',           # First by total score
                '-accuracy',        # Then by accuracy percentage
                'total_attempts',   # Then by fewer attempts (more efficient)
                'last_attempt'      # Finally by who completed first
            )[:10]

            return Response({
                "status": "success",
                "leaderboard": list(leaderboard_data)
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=500)

class QuestionDetail(APIView):
    def get(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
            question_data = {
                'id': question.id,
                'question_text': question.question_text,
                'options': question.options
            }
            return Response({
                "status": "success",
                "question": question_data
            })
        except Question.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Question not found"
            }, status=status.HTTP_404_NOT_FOUND)

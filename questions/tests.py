from django.test import TestCase, Client
from django.urls import reverse
from .models import Question, QuestionAttempt
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.urls import re_path
from .consumers import QuizConsumer
import json

class QuizTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.question = Question.objects.create(
            question_text="What is 2+2?",
            options=["3", "4", "5", "6"],
            correct_answer="4"
        )

    def test_question_list(self):
        response = self.client.get(reverse('question-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['questions']), 1)

    def test_submit_answer(self):
        response = self.client.post(reverse('submit-answer'), {
            'question_id': self.question.id,
            'selected_answer': '4'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['is_correct'])

    def test_leaderboard(self):
        # Create some attempts
        QuestionAttempt.objects.create(
            question=self.question,
            user_ip='127.0.0.1',
            selected_answer='4',
            is_correct=True
        )
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['leaderboard']), 1)


class WebSocketTestCase(TestCase):
    async def test_websocket_connection(self):
        application = URLRouter([
            re_path(r'ws/quiz/$', QuizConsumer.as_asgi()),
        ])
        communicator = WebsocketCommunicator(application, "ws/quiz/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_websocket_message(self):
        application = URLRouter([
            re_path(r'ws/quiz/$', QuizConsumer.as_asgi()),
        ])
        communicator = WebsocketCommunicator(application, "ws/quiz/")
        await communicator.connect()
        
        # Test sending message
        await communicator.send_json_to({
            "type": "answer_submitted",
            "user_ip": "127.0.0.1",
            "is_correct": True
        })
        
        response = await communicator.receive_json_from()
        self.assertIn("type", response)
        await communicator.disconnect()


class DatabaseTestCase(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            question_text="What is Python?",
            options=["Language", "Snake", "Both", "None"],
            correct_answer="Both"
        )

    def test_multiple_attempts(self):
        # Create multiple attempts from different IPs
        QuestionAttempt.objects.create(
            question=self.question,
            user_ip='192.168.1.1',
            selected_answer='Both',
            is_correct=True
        )
        QuestionAttempt.objects.create(
            question=self.question,
            user_ip='192.168.1.2',
            selected_answer='Snake',
            is_correct=False
        )

        # Test leaderboard ordering
        response = self.client.get(reverse('leaderboard'))
        leaderboard = response.data['leaderboard']
        self.assertEqual(len(leaderboard), 2)
        self.assertTrue(leaderboard[0]['score'] > leaderboard[1]['score'])

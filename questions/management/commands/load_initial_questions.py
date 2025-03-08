from django.core.management.base import BaseCommand
from questions.models import Question

class Command(BaseCommand):
    help = 'Loads initial programming questions'

    def handle(self, *args, **kwargs):
        questions_data = [
            {
                "question_text": "What is the primary purpose of the 'self' parameter in Python class methods?",
                "options": ["To create a new instance", "To reference the current instance", "To define class variables", "To import modules"],
                "correct_answer": "To reference the current instance"
            },
            {
                "question_text": "Which data structure in Python uses LIFO (Last In, First Out)?",
                "options": ["Queue", "Stack", "List", "Dictionary"],
                "correct_answer": "Stack"
            },
            {
                "question_text": "What is the output of print(type(1/2)) in Python 3?",
                "options": ["<class 'int'>", "<class 'float'>", "<class 'number'>", "<class 'decimal'>"],
                "correct_answer": "<class 'float'>"
            },
            {
                "question_text": "Which of these is NOT a valid variable name in Python?",
                "options": ["my_var", "_variable", "2variable", "variable2"],
                "correct_answer": "2variable"
            },
            {
                "question_text": "What does REST stand for in REST API?",
                "options": ["Remote State Transfer", "Representational State Transfer", "Remote System Transfer", "Representational System Transfer"],
                "correct_answer": "Representational State Transfer"
            },
            {
                "question_text": "Which HTTP method is idempotent?",
                "options": ["POST", "GET", "PATCH", "DELETE"],
                "correct_answer": "GET"
            },
            {
                "question_text": "What is the time complexity of binary search?",
                "options": ["O(n)", "O(n²)", "O(log n)", "O(1)"],
                "correct_answer": "O(log n)"
            },
            {
                "question_text": "Which of these is not a principle of OOP?",
                "options": ["Inheritance", "Encapsulation", "Sequencing", "Polymorphism"],
                "correct_answer": "Sequencing"
            },
            {
                "question_text": "What does Django use for its database ORM?",
                "options": ["Models", "Views", "Templates", "Forms"],
                "correct_answer": "Models"
            },
            {
                "question_text": "Which of these is not a valid HTTP status code?",
                "options": ["200", "404", "600", "500"],
                "correct_answer": "600"
            }
        ]

        for question_data in questions_data:
            Question.objects.create(
                question_text=question_data['question_text'],
                options=question_data['options'],
                correct_answer=question_data['correct_answer']
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded initial questions'))
from django.core.management.base import BaseCommand
from questions.models import Question

class Command(BaseCommand):
    help = 'Loads initial GK questions'

    def handle(self, *args, **kwargs):
        questions_data = [
            {
                "id": 1,
                "question_text": "Which is the largest planet in our solar system?",
                "options": ["Mars", "Jupiter", "Saturn", "Neptune"],
                "correct_answer": "Jupiter"
            },
            {
                "id": 2,
                "question_text": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct_answer": "Paris"
            },
            {
                "id": 3,
                "question_text": "Who wrote 'Romeo and Juliet'?",
                "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                "correct_answer": "William Shakespeare"
            },
            {
                "id": 4,
                "question_text": "What is the chemical symbol for Gold?",
                "options": ["Au", "Ag", "Fe", "Cu"],
                "correct_answer": "Au"
            },
            {
                "id": 5,
                "question_text": "Which is the largest ocean on Earth?",
                "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
                "correct_answer": "Pacific"
            },
            {
                "id": 6,
                "question_text": "In which year did World War II end?",
                "options": ["1943", "1944", "1945", "1946"],
                "correct_answer": "1945"
            },
            {
                "id": 7,
                "question_text": "What is the fastest land animal?",
                "options": ["Lion", "Cheetah", "Tiger", "Leopard"],
                "correct_answer": "Cheetah"
            },
            {
                "id": 8,
                "question_text": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Mercury", "Jupiter"],
                "correct_answer": "Mars"
            },
            {
                "id": 9,
                "question_text": "Who painted the Mona Lisa?",
                "options": ["Van Gogh", "Da Vinci", "Picasso", "Michelangelo"],
                "correct_answer": "Da Vinci"
            },
            {
                "id": 10,
                "question_text": "What is the largest continent?",
                "options": ["North America", "Europe", "Africa", "Asia"],
                "correct_answer": "Asia"
            }
        ]

        # Clear existing questions
        Question.objects.all().delete()

        for question_data in questions_data:
            Question.objects.create(
                id=question_data['id'],
                question_text=question_data['question_text'],
                options=question_data['options'],
                correct_answer=question_data['correct_answer']
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded GK questions'))
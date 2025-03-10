from django.core.management.base import BaseCommand
from users.models import UserProfile
from questions.models import Question
from answers.models import Answer

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # First load questions
        try:
            from questions.management.commands.load_initial_questions import Command as LoadQuestionsCommand
            LoadQuestionsCommand().handle()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading questions: {e}'))
            return

        # Create or get test users
        users = []
        for i in range(1, 4):
            try:
                user, created = UserProfile.objects.get_or_create(
                    email=f"user{i}@test.com",
                    defaults={
                        'first_name': f"User{i}",
                        'last_name': "Test",
                        'phone_number': f"123456789{i}",
                        'password': "test123"
                    }
                )
                users.append(user)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new user {user.email}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Using existing user {user.email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error with user {i}: {e}'))

        # Submit answers
        questions = Question.objects.all()
        for user in users:
            for question in questions:
                try:
                    Answer.objects.get_or_create(
                        user=user,
                        question=question,
                        defaults={
                            'selected_answer': question.correct_answer,
                            'is_correct': True
                        }
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating answer: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
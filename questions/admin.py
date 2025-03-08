from django.contrib import admin
from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'correct_answer')
    
    def save_model(self, request, obj, form, change):
        if not obj.options:  # if options is empty
            obj.options = ["Option 1", "Option 2", "Option 3", "Option 4"]
        super().save_model(request, obj, form, change)

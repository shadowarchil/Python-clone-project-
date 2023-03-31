from django import forms
from core.models import Question,Answer
from typing import Any

class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        # fields = '__all__'
        exclude = ['user', 'views']
    
    def __init__(self, *args, **kwargs) -> None:
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, commit: bool = ...) -> Any:
        question: Question = super().save(commit=False)
        question.user = self.user
        question.save()
        return question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        

    
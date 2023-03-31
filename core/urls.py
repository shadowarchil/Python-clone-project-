from django.urls import path
from core.views import HomeView, QuestionDetailView, QuestionCreateView, QuestonDeleteView, QuestionUpdateView,AnswerCreateView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('question<tag>/', HomeView.as_view(), name='question-by-tag'), #
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('questions/<int:pk>/delete/', QuestonDeleteView.as_view(), name='question-delete'),
    path('questions/<int:pk>/update/', QuestionUpdateView.as_view(), name='question-update'),
    path('questions/<int:question_id>/answer/', AnswerCreateView.as_view(), name='answer-create'),
    path('ask/', QuestionCreateView.as_view(), name='question-create')
    

]
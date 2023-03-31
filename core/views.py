from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Question,Answer
from core.models import Tag
from core.forms import QuestionCreateForm,AnswerForm
from django.urls import reverse_lazy, reverse
from typing import Dict, Any
from django.db.models import Q


def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html', context={
        'questions': Question.objects.all()
    })


class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'questions'
    ordering = ['-create_time']
    paginate_by = 5
# sort by Tag
    def get_queryset(self):
        search_term = self.request.GET.get('q', '')
        tag = self.kwargs.get('tag')
        queryset = Question.objects.all()
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(user__username__icontains=search_term)
            )
        if tag:
            tagObject = Tag.objects.filter(title=tag).first()
            queryset = queryset.filter(tags=tagObject)
        return queryset.order_by(*self.get_ordering())
    




class QuestionDetailView(DetailView):
    template_name = 'question_detail.html'
    model = Question

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        answer_form = None
        if not request.session.get('has_viewed_question_{}'.format(self.object.pk), False):
            self.object.increase_views()
            request.session['has_viewed_question_{}'.format(self.object.pk)] = True
            answer_form = AnswerForm()
        context = self.get_context_data(object=self.object, answer_form=answer_form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.user = request.user
            answer.question = self.object
            answer.save()
            return redirect('core:question-detail', pk=self.object.pk)
        context = self.get_context_data(object=self.object, answer_form=answer_form)
        return self.render_to_response(context)
    
     #  answer form to  answer users questions
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'answer_form' not in kwargs or kwargs['answer_form'] is None:
            context['answer_form'] = AnswerForm()
        return context
    
    
# def question_detail(request, question_id):
#         question = get_object_or_404(Question, id=question_id)
#         answer_form = AnswerForm()
#         context = {'question': question, 'answer_form': answer_form}
#         return render(request, 'question_detail.html', context)




class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'question_create.html'
    success_url = reverse_lazy('core:home')

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.tags.add(
            *[tag.id for tag in form.cleaned_data['tags']]
        )
        return super().form_valid(form)
        


class QuestonDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'question_delete.html'
    success_url = reverse_lazy('core:home')

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user)


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'question_update.html'
    fields = [ 'tags', 'title', 'text']

    def get_success_url(self) -> str:
        return reverse('core:question-detail', kwargs={'pk': self.get_object().pk})

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user)


class AnswerCreateView(CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'answer_create.html'

    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        answer = form.save(commit=False)
        answer.user = self.request.user
        answer.question = question
        answer.save()
        return redirect('core:question-detail', pk=question.pk)



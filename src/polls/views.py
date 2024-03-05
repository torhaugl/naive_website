from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from physmet.django.views import AppView
from physmet.django.decorators import azure_login_required
from django.utils.decorators import method_decorator

from .models import Question, Choice


@method_decorator(azure_login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.all()


@method_decorator(azure_login_required, name='dispatch')
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"



@azure_login_required
def vote(request, question_id):
    # vote on question
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_msg": "Selected choice does not exist"},
        )

    selected_choice.votes += 1
    selected_choice.save()

    return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))



class ResultsView(AppView):
    name = 'results'
    path = 'results'
    template = 'polls/results'
    login_required = True
    roles_required = {
        'get': 'portal-read | portal-admin',
        'post': 'portal-admin'
    }

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        self["question"] = question
        return self.render(request)

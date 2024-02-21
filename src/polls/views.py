from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from physmet.PhysMetAppView import PhysMetAppView

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.all()


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(request.POST)
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

class ResultsView(PhysMetAppView):
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

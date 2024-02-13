from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.conf import settings

from .models import Question, Choice

try:
    ms_identity_web = settings.MS_IDENTITY_WEB
except:
    class TempClass:
        def login_required(self, f):
            return f
    ms_identity_web = TempClass()


@ms_identity_web.login_required
class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.all()


@ms_identity_web.login_required
class DetailView(generic.DetailView):
    model = Question
    template_name = "detail.html"


@ms_identity_web.login_required
class ResultView(generic.DetailView):
    model = Question
    template_name = "results.html"


@ms_identity_web.login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(request.POST)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "detail.html",
            {"question": question, "error_msg": "Selected choice does not exist"},
        )

    selected_choice.votes += 1
    selected_choice.save()

    return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))

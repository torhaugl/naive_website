from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.conf import settings
from django.utils.decorators import method_decorator
from physmet_portal.dashboard.views import PhysMetAppView

from .models import Question, Choice

try:
    ms_identity_web = settings.MS_IDENTITY_WEB
except:
    class TempClass:
        def login_required(self, f):
            return f
    ms_identity_web = TempClass()


@method_decorator(ms_identity_web.login_required, name="dispatch")
class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.all()


@method_decorator(ms_identity_web.login_required, name="dispatch")
class DetailView(generic.DetailView):
    model = Question
    template_name = "detail.html"


#@method_decorator(ms_identity_web.login_required, name="dispatch")
#class ResultView(generic.DetailView):
#    model = Question
#    template_name = "results.html"

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

class ResultsView(PhysMetAppView):
    name = 'results'
    path = 'results'
    template = 'results'
    login_required = True
    roles_required = {
        'get': 'portal-read | portal-admin',
        'post': 'portal-admin'
    }

    def get(self, request, question_id):
        print(request)
        question = get_object_or_404(Question, pk=question_id)
        self.context["question"] = question
        #return render(request, "polls/results.html", {"question": question})
        return self.render(request)

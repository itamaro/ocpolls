# Create your views here.
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView
from polls.forms import CreatePollForm
from polls.models import Poll, Vote
import json


class HomeView(CreateView):
    model = Poll
    form_class = CreatePollForm

    def form_valid(self, form):
        form.instance.proposals = form.cleaned_data['text'].splitlines()
        return super(HomeView, self).form_valid(form)


class PollView(DetailView):
    model = Poll

    def post(self, request, *args, **kwargs):
        o = Vote(poll=self.get_object())
        o.data = json.loads(request.POST['vote'])
        o.save()
        return redirect(o.poll.get_result_url())


class ResultView(DetailView):
    model = Poll
    template_name = "polls/poll_result.html"

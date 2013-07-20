from annoying.fields import JSONField
from django.db import models
from polls.graphs import DynamicSchulze
import json


class Poll(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    proposals = JSONField()
    # result = models.TextField(null=True, blank=True)

    def calculate_result(self):
        valid_props = range(len(self.proposals))
        schulze = DynamicSchulze(valid_props)
        for v in self.votes.all():
            schulze.add_vote(v.data)
        result = schulze.run_schulze()
        return [set([self.proposals[i] for i in x]) for x in result]

    @models.permalink
    def get_absolute_url(self):
        return 'poll', (str(self.id),)

    @models.permalink
    def get_result_url(self):
        return 'poll_result', (str(self.id),)

    def json_proposals(self):
        return json.dumps(self.proposals)


class Vote(models.Model):
    poll = models.ForeignKey(Poll, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)
    data = JSONField()

    def as_stringlist(self):
        return [[self.poll.proposals[i] for i in x] for x in self.data]

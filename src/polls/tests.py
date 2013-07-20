from django.test import TestCase
from polls.models import Poll, Vote


class PollTest(TestCase):

    def test_basic_poll(self):

        props = ['Red', 'Blue', 'Green']

        p = Poll.objects.create(proposals=props)

        Vote.objects.create(poll=p, data=[[0, 1, 2]])
        Vote.objects.create(poll=p, data=[[0], [1, 2]])
        Vote.objects.create(poll=p, data=[[1, 2], [0]])
        Vote.objects.create(poll=p, data=[[2], [1, 0]])
        Vote.objects.create(poll=p, data=[[0, 1, 2]])

        self.assertEquals(5, p.votes.count())
        self.assertEquals(p.calculate_result(), [set(['Green']), set(['Red']), set(['Blue'])])

    def test_poll_tie(self):

        props = ['Red', 'Blue', 'Green']

        p = Poll.objects.create(proposals=props)

        Vote.objects.create(poll=p, data=[[0, 1, 2]])
        Vote.objects.create(poll=p, data=[[0, 1, 2]])
        Vote.objects.create(poll=p, data=[[0, 1, 2]])

        self.assertEquals(3, p.votes.count())
        self.assertEquals(p.calculate_result(), [set(['Green', 'Red', 'Blue'])])

    def test_poll_strange(self):

        props = ['A', 'B', 'C', 'D', 'E']

        p = Poll.objects.create(proposals=props)

        votes = [
                    [[0, 1, 2, 3, 4]],
                    [[0], [1, 2, 3, 4]],
                    [[1, 2, 3, 4], [0]],
                    [[3], [0, 1, 2, 4]],
                ]

        for v in votes:
            Vote.objects.create(poll=p, data=v)

        self.assertEquals(len(votes), p.votes.count())
        self.assertEquals([set(['D']), set(['A','B','C','D'])],
                               p.calculate_result())
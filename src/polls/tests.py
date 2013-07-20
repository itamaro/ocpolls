from django.test import TestCase
from polls.models import Poll, Vote
import unittest

class PollTest(TestCase):

    def _test_poll(self, props, votes, result):

        p = Poll.objects.create(proposals=props)

        for v in votes:
            Vote.objects.create(poll=p, data=v)

        self.assertEquals(len(votes), p.votes.count())

        expected = [set(x) for x in result]

        self.assertEquals(expected, p.calculate_result())

        return p

    def test_basic_poll(self):

        props = ['Red', 'Blue', 'Green']

        votes = (
            [[0, 1, 2]],
            [[0], [1, 2]],
            [[1, 2], [0]],
            [[2], [1, 0]],
            [[0, 1, 2]],
        )

        result = [
                  ['Green'],
                  ['Red'],
                  ['Blue']
                 ]

        p = self._test_poll(props, votes, result)

    def test_poll_tie(self):

        props = ['Red', 'Blue', 'Green']

        votes = [
            [[0, 1, 2]],
            [[0, 1, 2]],
            [[0, 1, 2]],
        ]

        result = [
                  ['Green', 'Red', 'Blue'],
                 ]

        p = self._test_poll(props, votes, result)

    @unittest.expectedFailure
    def test_poll_strange(self):

        props = ['A', 'B', 'C', 'D', 'E']

        votes = [
                    [[0, 1, 2, 3, 4]],
                    [[0], [1, 2, 3, 4]],
                    [[1, 2, 3, 4], [0]],
                    [[3], [0, 1, 2, 4]],
                ]

        result = [
                  ['D'],
                  ['A', 'B', 'C', 'E']
                 ]

        p = self._test_poll(props, votes, result)

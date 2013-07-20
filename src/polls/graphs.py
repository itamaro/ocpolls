import copy
from pyvotecore.schulze_pr import SchulzePR
from pyvotecore.schulze_method import SchulzeMethod

###################################
#
# Single vote format:
# List of lists, ordered by priority.
# Every item in the list are numbers from 0 to N-1, inclusive. All values from 0 to N-1 must be included.
#
# Examples:
# vote = [ [0], [1,2], [3] ] # good
# vote = [ 0, [1,2], [3] ] # bad
# vote = [ (0), [1,2], [3] ] # bad
# vote = ( [0], [1,2], [3] ) # bad
# vote = [ [0], [2,1], [3] ] # good
# vote = [ [0], [1,2], [2,3] ] # bad
# vote = [ [0], [1,2], [4] ] # bad
# vote = [ [4], [1,2], [3] ] # bad

class DynamicSchulze(object):

    def __init__(self, candidates):
        self.hist = dict()
        assert type(candidates) in [list, set, tuple]
        self.candidates = set(candidates)
        self.vote_count = 0
        self.schulze_method_result = None
        self.schulze_pr_result = None

    def add_vote(self, vote):
        # Invalidate results cache
        self.invalidate_cache()
        # verify valid permutation
        perm = sum(vote, [])
        perm.sort()
        seen = set()
        for c in perm:
            if not (c in self.candidates) or (c in seen):
                raise Exception("Invalid vote", vote)
            seen.add(c)
        # sort internal-lists
        in_vote = list()
        for sub_v in vote:
            in_vote.append(tuple(sorted(sub_v)))
        self.vote_count += 1
        in_vote = tuple(in_vote)
        if in_vote in self.hist:
            self.hist[in_vote] += 1
        else:
            self.hist[in_vote] = 1

    def get_schulze_format(self):
        out = list()
        for vote, count in self.hist.iteritems():
            out.append({'count': count, 'ballot': list(vote)})
        return out

    def get_vote_count(self):
        return self.vote_count
    
    def validate_cache(self):
        if self.schulze_method_result is None or self.schulze_pr_result is None:
            schulze_format = self.get_schulze_format()
        if self.schulze_method_result is None:
            self.schulze_method_result = SchulzeMethod(copy.deepcopy(schulze_format), ballot_notation="grouping").as_dict()
        if self.schulze_pr_result is None:
            self.schulze_pr_result = SchulzePR(copy.deepcopy(schulze_format), ballot_notation="grouping").as_dict()
    
    def invalidate_cache(self):
        self.schulze_method_result = None
        self.schulze_pr_result = None

    def get_order(self):
        self.validate_cache()
        # convert resulting order to ordered sets of tied winners
        seen = set()
        order = list()
        for winner in self.schulze_pr_result['rounds']:
            if winner['winner'] in seen:
                continue
            tied = set((winner['winner'],))
            if 'tied_winners' in winner:
                tied = tied.union(winner['tied_winners'])
            seen = seen.union(tied)
            order.append(tied)
        return order
        
    def get_pairs_matrix(self):
        self.validate_cache()
        dim = len(self.candidates)
        labels = dict()
        matrix = list()
        for idx, c in enumerate(self.candidates):
            labels[c] = idx
            matrix.append([None] * dim)
        for pair, count in self.schulze_method_result['pairs'].iteritems():
            row_id = labels[pair[0]]
            col_id = labels[pair[1]]
            matrix[row_id][col_id] = count
        return labels, matrix

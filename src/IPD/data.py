from copy import deepcopy
from random import randint


class Player(object):
    def __init__(self, score=0):
        self.name = None
        self.score = score
        self.last_action = None
        self.this_action = None
        self.opponent = None

    def _match_reset(self):
        self.history = []
        self.score = 0
        self.init_match()

    def init_match(self):
        """Runs before the start of a new match. Reset any variables here!
        """
        pass

    def reset_score(self):
        self.score = 0

    def _action(self, opponent):
        self.this_action = self.action(opponent)
        return self.this_action

    def action(self, opponent):
        return True

    def update_history(self):
        self.history.append(self.this_action)

    def add_points(self, points):
        self.score += points


# -------------------------------------------------- #

class Population(object):
    def __init__(self, members: list):
        self.members = members

    def __repr__(self):
        return "{}".format(self.members)

    def __iter__(self):
        return iter(self.members)

    def __len__(self):
        return len(self.members)

    def __getitem__(self, item):
        return self.members[item]

    def append(self, member):
        self.members.append(member)

    def scores(self):
        return [member.score for member in self.members]

    def reset_all_scores(self):
        for member in self.members:
            member.reset_score()

    def first_member(self):
        return self.members[0]

    def excluding(self, excluded_member):
        copy = self.members[:]
        return Population([member for member in copy if member is not excluded_member])

    def is_empty(self):
        return not self.members

    def total_score(self):
        total = 0
        for member in self.members:
            total += member.score
        return total

    def create_next_gen(self):
        """ Example --
        Population is comprised of Player 1 and Player 2.
        Player 1 has a final score of 10. Player 2 has a final score of 20.
        Each new member of the new generation has a 33% chance (1/3) chance of being an
        offspring of Player 1, and a 67% chance (2/3) of being an offspring of Player 2.
        """
        next_gen = Population([])
        total_score = self.total_score()
        for i in range(len(self.members)):
            rand = randint(1, total_score)
            curr = 0
            for member in self.members:
                curr += member.score
                if rand <= curr:
                    next_gen.append(deepcopy(member))
                    break
        next_gen.reset_all_scores()
        return next_gen

    def distribution(self):
        dist = {}
        total_num_players = 0
        for member in self.members:
            if member.name in dist:
                dist[member.name] += 1
            else:
                dist[member.name] = 1
            total_num_players += 1
        for member in dist:
            prop = dist[member] / total_num_players * 100
            dist[member] = '%.2f' % prop
        return dist


from .data import Player


class Kantian(Player):
    """ Always cooperates. """
    def __init__(self, score=0):
        super().__init__()
        self.name = "Kantian"


class Defector(Player):
    """Always defects."""

    def __init__(self, score=0):
        super().__init__()
        self.name = "Defector"

    def action(self, opponent):
        return False


class TitForTat(Player):
    """Starts by cooperating. After that, always cooperates unless
    opponent's last move was defect."""
    first = True
    name = "Tit for Tat"

    def action(self, opponent):
        return opponent.history[-1]


class TitFor2Tats(Player):
    """Starts by cooperating. After that, always cooperates unless
    opponent's last two moves were defect."""
    first = True
    name = "Tit for 2 Tats"

    def action(self, opponent):
        return not (opponent.history[-3:-1] == [False, False])


class MeanTitForTat(TitForTat):
    """ Tit for Tat, but occasionally defects. """
    name = "Mean Tit for Tat"

    def action(self, opponent):
        return self.random(4/5) and super().action(opponent)


class WaryTitForTat(TitForTat):
    """ Tit for Tat, but starts by defecting. """
    name = "Wary Tit for Tat"
    first = False


class Tester(TitForTat):
    """ Tit for 2 Tats exploiter. Tit for Tat, but occasionally defects
    then cooperates for a turn. If the opponent doesn't retaliate immediately,
    alternates between cooperating and defecting. """
    name = "Tester"

    def action(self, opponent):
        self.turn += 1
        if self.testing_turn == 0 and self.random(1/5):
            self.testing_turn += 1
            return False
        elif 0 < self.testing_turn <= 1:
            self.testing_turn += 1
            if opponent.history and not opponent.history[-1]:
                self.opponent_retaliated = True
            return True
        elif self.testing_turn > 1 and not self.opponent_retaliated:
            return self.turn % 2
        else:
            return super().action(opponent)

    def init_match(self):
        self.turn = 0
        self.testing_turn = 0
        self.opponent_retaliated = False


class Conniver(TitForTat):
    """ Kantian exploiter. Tit for Tat, but occasionally defects then cooperates
    for 2 turns. If opponent doesn't retaliate within 2 turns, defects until end. """

    name = "Conniver"

    def action(self, opponent):
        if self.testing_turn == 0 and self.random(1/5):
            self.testing_turn += 1
            return False
        elif 0 < self.testing_turn <= 2:
            self.testing_turn += 1
            if opponent.history and not opponent.history[-1]:
                self.opponent_retaliated = True
            return True
        elif self.testing_turn > 2 and not self.opponent_retaliated:
            return False
        else:
            return super().action(opponent)

    def init_match(self):
        self.testing_turn = 0
        self.opponent_retaliated = False


class Grudger(Player):
    """ Cooperates until opponent defects. """
    first = True
    name = "Grudger"

    def action(self, opponent):
        if not opponent.history[-1]:
            self.opponent_never_defected = False
        return self.opponent_never_defected

    def init_match(self):
        self.opponent_never_defected = True


class Pavlovian(Player):
    """ Starts by cooperating. If points were gained in the last turn, repeats action.
    Otherwise does opposite action. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Pavlovian"
        self.last_score = 0

    def action(self, opponent):
        temp = self.last_score
        self.last_score = self.score
        if self.score > temp:
            return self.last_action
        else:
            return not self.last_action

    def init_match(self):
        self.last_action = True


class ClanGrunt(Player):
    """ Tit for Tat, but starts with sequence: DCCCD. If opponent starts with same
    sequence, cooperates until end. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Clan Grunt"


class ClanLeader(Player):
    """ Tit for Tat, but starts with sequence: DCCCD. If opponent starts with same
    sequence, defects until end. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Clan Leader"


class Random(Player):
    """ Cooperates or defects at 50/50. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Random"

    def action(self, opponent):
        return self.random(1/2)


class Grofman(Player):
    """Cooperates on the first turn. Then"""

    def __init__(self, score=0):
        super().__init__()
        self.name = "Grofman"

    def action(self, opponent):
        return len(self.history) == 0 or self.history[-1] == opponent.history[-1] or self.random(2 / 7)


all_strategies = {
    'Kantian': Kantian(),
    'Defector': Defector(),
    'Tit for Tat': TitForTat(),
    'Tit for 2 Tats': TitFor2Tats(),
    'Mean Tit for Tat': MeanTitForTat(),
    'Wary Tit for Tat': WaryTitForTat(),
    'Tester': Tester(),
    'Conniver': Conniver(),
    'Grudger': Grudger(),
    'Pavlovian': Pavlovian(),
    'Clan Grunt': ClanGrunt(),
    'Clan Leader': ClanLeader(),
    'Random': Random(),
    'Grofman': Grofman()
}
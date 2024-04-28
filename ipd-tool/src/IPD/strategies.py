from data import Player, randint

class Kantian(Player):
    """ Always cooperates. """
    name = "Kantain"
    # def __init__(self, score=0):
    #     super().__init__()
    #     self.name = "Kantian"


class Defector(Player):
    """Always defects."""

    def __init__(self, score=0):
        super().__init__()
        self.name = "Defector"

    def decide_action(self):
        return False


class TitForTat(Player):
    """Starts by cooperating. After that, always cooperates unless
    opponent's last move was defect."""

    def __init__(self, score=0):
        super().__init__()
        self.name = "Tit for Tat"
        self.is_first_move = True

    def decide_action(self):
        if not self.is_first_move:
            return self.opponent.last_action
        else:
            self.is_first_move = False
            return True

    def new_match_against(self, opponent):
        self.is_first_move = True
        super().new_match_against(opponent)


class TitFor2Tats(Player):
    """Starts by cooperating. After that, always cooperates unless
    opponent's last two moves were defect."""

    def __init__(self, score=0):
        super().__init__()
        self.name = "Tit for 2 Tats"
        self.opponent_last_actions = (True, True)

    def decide_action(self):
        if self.opponent.last_action is None:
            self.opponent_last_actions = (self.opponent_last_actions[1], True)
        else:
            self.opponent_last_actions =\
                (self.opponent_last_actions[1], self.opponent.last_action)
        return self.opponent_last_actions[0] or self.opponent_last_actions[1]

    def new_match_against(self, opponent):
        self.opponent_last_actions = (True, True)
        super().new_match_against(opponent)


class MeanTitForTat(TitForTat):
    """ Tit for Tat, but occasionally defects. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Mean Tit for Tat"

    def decide_action(self):
        if not randint(0, 5):
            return False
        else:
            return super().decide_action()


class WaryTitForTat(TitForTat):
    """ Tit for Tat, but starts by defecting. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Wary Tit for Tat"

    def decide_action(self):
        if self.is_first_move:
            self.is_first_move = False
            return False
        else:
            return super().decide_action()


class Tester(TitForTat):
    """ Tit for 2 Tats exploiter. Tit for Tat, but occasionally defects
    then cooperates for a turn. If the opponent doesn't retaliate immediately,
    alternates between cooperating and defecting. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Tester"
        self.turn = 0
        self.testing_turn = 0
        self.opponent_retaliated = False

    def decide_action(self):
        self.turn += 1
        if self.testing_turn == 0 and not randint(0, 5):
            self.testing_turn += 1
            return False
        elif 0 < self.testing_turn <= 1:
            self.testing_turn += 1
            if not self.opponent.last_action:
                self.opponent_retaliated = True
            return True
        elif self.testing_turn > 1 and not self.opponent_retaliated:
            return self.turn % 2
        else:
            return super().decide_action()

    def new_match_against(self, opponent):
        self.turn = 0
        self.testing_turn = 0
        self.opponent_retaliated = False
        return super().new_match_against(opponent)


class Conniver(TitForTat):
    """ Kantian exploiter. Tit for Tat, but occasionally defects then cooperates
    for 2 turns. If opponent doesn't retaliate within 2 turns, defects until end. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Conniver"
        self.testing_turn = 0
        self.opponent_retaliated = False

    def decide_action(self):
        if self.testing_turn == 0 and not randint(0, 5):
            self.testing_turn += 1
            return False
        elif 0 < self.testing_turn <= 2:
            self.testing_turn += 1
            if not self.opponent.last_action:
                self.opponent_retaliated = True
            return True
        elif self.testing_turn > 2 and not self.opponent_retaliated:
            return False
        else:
            return super().decide_action()

    def new_match_against(self, opponent):
        self.testing_turn = 0
        self.opponent_retaliated = False
        return super().new_match_against(opponent)


class Grudger(Player):
    """ Cooperates until opponent defects. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Grudger"
        self.opponent_never_defected = True

    def decide_action(self):
        if not self.opponent.last_action:
            self.opponent_never_defected = False
        return self.opponent_never_defected

    def new_match_against(self, opponent):
        self.opponent_never_defected = True
        super().new_match_against(opponent)


class Pavlovian(Player):
    """ Starts by cooperating. If points were gained in the last turn, repeats action.
    Otherwise does opposite action. """

    def __init__(self, score=0):
        super().__init__()
        self.name = "Pavlovian"
        self.last_score = 0

    def decide_action(self):
        temp = self.last_score
        self.last_score = self.score
        if self.score > temp:
            return self.last_action
        else:
            return not self.last_action

    def new_match_against(self, opponent):
        self.last_action = True
        super().new_match_against(opponent)


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

    def decide_action(self):
        return randint(0, 1)

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
    'Random': Random()
}
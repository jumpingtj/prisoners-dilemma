from itertools import combinations_with_replacement

def play_round(p1, p2):
    """ Payoffs:
        Both cooperate              -> both +2 pts
        Both defect                 -> both +1 pts
        One cooperates, one defects -> cooperator +0 pts, defector +3 pts
    """
    if not p1.history:
        p1_action, p2_action = p1._action(p2, True), p2._action(p1, True)
    else:
        p1_action, p2_action = p1._action(p2), p2._action(p1)

    if p1_action and p2_action:
        p1.add_points(2)
        p2.add_points(2)
    elif p1_action and not p2_action:
        p2.add_points(3)
    elif not p1_action and p2_action:
        p1.add_points(3)
    else:
        p1.add_points(1)
        p2.add_points(1)

    p1.update_history()
    p2.update_history()


def play_several_rounds(p1, p2, num_rounds):
    p1._match_reset()
    p2._match_reset()
    for i in range(num_rounds):
        play_round(p1, p2)


def round_robin(population, num_rounds):
    """Competes every member of the population with every other member
    of the population for num_rounds each.
    """
    if not population.is_empty():
        for match in combinations_with_replacement(population, 2):
            play_several_rounds(match[0], match[1], num_rounds)

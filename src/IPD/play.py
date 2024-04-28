def play_round(p1, p2):
    """ Payoffs:
        Both cooperate              -> both +2 pts
        Both defect                 -> both +1 pts
        One cooperates, one defects -> cooperator +0 pts, defector +3 pts
    """
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
        other_members = population.excluding(population.first_member())
        for member in other_members:
            play_several_rounds(population.first_member(), member, num_rounds)
        round_robin(other_members, num_rounds)

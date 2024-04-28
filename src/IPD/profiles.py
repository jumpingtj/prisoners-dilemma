from .strategies import *


def diverse():
    n = 15
    profile = {
        'Kantian': n,
        'Defector': n,
        'Tit for Tat': n,
        'Tit for 2 Tats': n,
        'Mean Tit for Tat': n,
        'Wary Tit for Tat': n,
        'Tester': n,
        'Conniver': n,
        'Grudger': n,
        'Pavlovian': n,
        'Random': n
    }
    return profile


def defectors_with_a_tft():
    profile = {
        'Defector': 50,
        'Tit for Tat': 1
    }
    return profile


def defectors_with_some_tft():
    profile = {
        'Defector': 50,
        'Tit for Tat': 5
    }
    return profile


def kantian_with_few_defectors():
    profile = {
        'Kantian': 50,
        'Defector': 3
    }
    return profile


def tfts_with_tester():
    profile = []
    for i in range(50):
        profile.append(TitForTat())
        profile.append(TitFor2Tats())
        profile.append(MeanTitForTat())
        profile.append(Tester())
        profile.append(Conniver())

    return Population(profile)


def tft_test1():
    profile = []
    for i in range(1):
        profile.append(TitForTat())
        profile.append(TitFor2Tats())
        profile.append(Grudger())
        profile.append(MeanTitForTat())
        profile.append(Tester())
        profile.append(Conniver())
    return Population(profile)

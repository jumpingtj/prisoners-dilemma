from .strategies import all_strategies
from .profiles import *
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from .data import Population
from .play import *

NUM_GENS = 35
NUM_ROUNDS = 100
INITIAL_PROFILE = defectors_with_some_tft()


def run_simulation(init_profile: dict, num_gens, num_rounds):
    dist = {
        'gens': np.linspace(1, num_gens, num_gens)
    }
    init_gen = populate(init_profile)
    init_dist = init_gen.distribution()
    # print(init_dist)
    for strat in init_profile:
        dist[strat] = np.zeros(num_gens)
        dist[strat][0] = init_dist[strat]
    curr_gen = init_gen
    for gen in range(num_gens):
        curr_gen, curr_dist = update_gen_dist(curr_gen, num_rounds)
        for strat in init_profile:
            if strat not in curr_dist:
                dist[strat][gen] = 0
            else:
                dist[strat][gen] = curr_dist[strat]
    return dist


def plot(simulation_results: dict):
    x_axis = simulation_results.pop('gens')
    for strat in simulation_results:
        plt.plot(x_axis, simulation_results[strat], label=strat)
    plt.title('Changes to population distribution with respect to time')
    plt.xlabel('Generation')
    plt.ylabel('Population Distribution [%]')
    plt.legend()
    plt.show()


def populate(input_dict):
    """ Example --
    >>> sample_dict = {
            'Kantian': 2,
            'Defector': 1
        }
    >>> sample_population = populate(sample_dict)

    is the same as doing:

    >>> sample_list = [Kantian(), Kantian(), Defector()]
    >>> sample_population = Population(sample_list)
    """
    profile = []
    for strategy in input_dict:
        if strategy not in all_strategies:
            raise Exception('Specified strategy does not exist.')
        else:
            for i in range(input_dict[strategy]):
                profile.append(deepcopy(all_strategies[strategy]))
    return Population(profile)


def update_gen_dist(curr_gen, num_rounds):
    round_robin(curr_gen, num_rounds)
    new_gen = curr_gen.create_next_gen()
    new_dist = new_gen.distribution()
    return new_gen, new_dist


if __name__ == '__main__':
    a = run_simulation(INITIAL_PROFILE, NUM_GENS, NUM_ROUNDS)
    plot(a)

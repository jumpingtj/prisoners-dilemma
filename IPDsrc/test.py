class Population(object):
    """An object that represents a generation of players. Contains all players
    in a list."""
    def __init__(self, members):
        self.members = members

    def __repr__(self):
        return "{}".format(self.members)

    def get_members(self):
        return self.members

    def first_member(self):
        if not self.members:
            raise Exception("There are no players in this population.")
        else:
            return self.members[0]

    def excluding(self, excluded_member):
        copy = self.members[:]
        return [member for member in copy if member is not excluded_member]


class Number(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "{}".format(self.value)


def round_robin(population):
    """Competes each player in population against every other player in population.
    >>> p1 = Number(1)
    >>> p2 = Number(2)
    >>> p3 = Number(3)
    >>> p4 = Number(4)
    >>> p5 = Number(5)
    >>> members = [p1, p2, p3, p4, p5]
    >>> population = Population(members)
    >>> print([member.value for member in population.get_members()])
    [1, 2, 3, 4, 5]
    >>> round_robin(population)
    >>> print([member.value for member in population.get_members()])
    [15, 15, 15, 15, 15]
    """
    return None


def interact(p1, p2):
    sum = p1.value + p2.value
    p1.value, p2.value = sum, sum


#############
## Testing ##
#############

print("Initial state:")
p1 = Number(1)
p2 = Number(2)
p3 = Number(3)
p4 = Number(4)
p5 = Number(5)
members = [p1, p2, p3, p4, p5]
population = Population(members)
print(population)

print("Members not including first:")
other_members = population.excluding(population.first_member())
print(other_members)





######################
## Running Doctests ##
######################

# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
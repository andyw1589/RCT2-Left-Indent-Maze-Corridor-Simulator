"""
Calculate probabilities of where a guest will end up after n steps, starting in the middle of
a left-indent maze corridor facing upwards.
"""
from math import isclose
from pprint import pprint

steps = {
    "U": {"L": .75, "U": .25},
    "L": {"R": 1},
    "D": {"L": .25, "D": .75},
    "R": {"U": .5, "D": .5}
}


def get_all_paths(n: int) -> list[str]:
    """
    Given # of steps n, return a list of all possible sequence of steps a guest can take

    Preconditions:
      - n >= 0

    >>> set(get_all_paths(3)) == {"UUU", "UUL", "ULR", "LRU", "LRD"}
    True
    """
    assert n >= 0
    return get_all_paths_rec("L", n) + get_all_paths_rec("U", n)


def get_all_paths_rec(c: str, n: int) -> list[str]:
    """
    Given # of steps n, and previous character c representing the first move, return a list
    of all possible sequence of steps a guest can take, starting with c

    Preconditions:
      - n >= 0
      - c in steps
    """
    assert n >= 0
    assert c in steps

    paths = []

    if n == 0:
        return []
    elif n == 1:
        return [c]
    else:
        for step in steps[c]:
            paths += [c + path for path in get_all_paths_rec(step, n - 1)]

        return paths


def calculate_probability(path: str) -> float:
    """
    Given a path, return the probability that a guest will take that path.

    >>> import math
    >>> math.isclose(calculate_probability("LRD"), .375)
    True
    >>> math.isclose(calculate_probability("UUL"), .25 * .25 * .75)
    True
    """
    total_probability = 1

    for i in range(len(path)):
        step = path[i]

        # initial probabilities
        if i == 0:
            total_probability *= steps["U"][step]
        else:
            total_probability *= steps[path[i - 1]][step]

    return total_probability


def get_probability_map(n: int) -> dict:
    """
    Given # of steps n, return a mapping from progress to probability that a guest will make
    that much progress.

    >>> import math
    >>> get_probability_map(3) == {-1: 0.375, 1: 0.5625, 2: 0.046875, 3: 0.015625}
    True
    """
    progress_map = {}

    for path in get_all_paths(n):
        progress = path.count("U") - path.count("D")
        probability = calculate_probability(path)

        if progress not in progress_map:
            progress_map[progress] = 0
        progress_map[progress] += probability

    assert isclose(sum(progress_map.values()), 1)
    return progress_map


if __name__ == "__main__":
    mapping = get_probability_map(15)
    pprint(mapping)

    # Get the total probability of moving backwards
    total_prob = sum(mapping[progress] for progress in mapping.keys() if progress <= 0)

    # High probability of moving backwards if the # of steps is high
    print(total_prob)

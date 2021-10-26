from collections import Counter
from itertools import combinations, combinations_with_replacement
from scipy.stats import binom
import json
import random
import pandas as pd

BONUS = {"para": 0, "dpary": 0, "trojka": 0, "maly strit": 0, "duzy strit": 0,
         "full": 30, "kareta": 40, "general": 50}

def gorna(x, counter):
    return x * (counter[x] - 3)


def para(counter):
    atleasttwo = [el for el in counter if counter[el] >= 2]
    if len(atleasttwo) >= 1:
        return 2 * max(atleasttwo) + BONUS["para"]
    else:
        return 0


def dpary(counter):
    atleasttwo = [el for el in counter if counter[el] >= 2]
    if len(atleasttwo) == 2:
        x = max(atleasttwo)
        y = min(atleasttwo)
        return 2 * (x + y) + BONUS["dpary"]
    else:
        return 0


def trojka(counter):
    atleastthree = [el for el in counter if counter[el] >= 3]
    if len(atleastthree) == 1:
        return 3 * max(atleastthree) + BONUS["trojka"]
    else:
        return 0


def maly_strit(counter):
    if set(counter.keys()) == {1, 2, 3, 4, 5}:
        return 15 + BONUS["maly strit"]
    else:
        return 0


def duzy_strit(counter):
    if set(counter.keys()) == {2, 3, 4, 5, 6}:
        return 20 + BONUS["duzy strit"]
    else:
        return 0


def full(counter):
    exactlytwo = [el for el in counter if counter[el] == 2]
    exactlythree = [el for el in counter if counter[el] == 3]
    if len(exactlytwo) == 1 and len(exactlythree) == 1:
        x = max(exactlythree)
        y = max(exactlytwo)
        return 3 * x + 2 * y + BONUS["full"]
    else:
        return 0


def kareta(counter):
    atleastfour = [el for el in counter if counter[el] >= 4]
    if len(atleastfour) == 1:
        return 4 * max(atleastfour) + BONUS["kareta"]
    else:
        return 0


def general(counter):
    atleastfive = [el for el in counter if counter[el] >= 5]
    if len(atleastfive) == 1:
        return 5 * max(atleastfive) + BONUS["general"]
    else:
        return 0


def ratunek(counter):
    score = 0
    for el in counter:
        score += el * counter[el]
    return score


def get_average(start_from, n):
    scores = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0,
              "para": 0, "dwie pary": 0, "trojka": 0, "maly strit": 0, "duzy strit": 0, "full": 0,
              "kareta": 0, "general": 0, "ratunek": 0}
    to_roll = 5 - len(start_from)

    for i in range(n):
        throw = random.choices(range(1, 7), k=to_roll)
        counter = Counter(throw + list(start_from))
        scores["1"] += score.gorna(1, counter)/n
        scores["2"] += score.gorna(2, counter)/n
        scores["3"] += score.gorna(3, counter)/n
        scores["4"] += score.gorna(4, counter)/n
        scores["5"] += score.gorna(5, counter)/n
        scores["6"] += score.gorna(6, counter)/n
        scores["para"] += score.para(counter)/n
        scores["dwie pary"] += score.dpary(counter)/n
        scores["trojka"] += score.trojka(counter)/n
        scores["maly strit"] += score.maly_strit(counter)/n
        scores["duzy strit"] += score.duzy_strit(counter)/n
        scores["full"] += score.full(counter)/n
        scores["kareta"] += score.kareta(counter)/n
        scores["general"] += score.general(counter)/n
        scores["ratunek"] += score.ratunek(counter)/n

    return scores


def get_max():
    return {"1": 2, "2": 4, "3": 6, "4": 8, "5": 10, "6": 12,
            "para": 12 + BONUS["para"], "dwie pary": 22 + BONUS["dpary"],
            "trojka": 18 + BONUS["trojka"], "maly strit": 15 + BONUS["maly strit"],
            "duzy strit": 20 + BONUS["duzy strit"], "full": 28 + BONUS["full"],
            "kareta": 24 + BONUS["kareta"], "general": 30 + BONUS["general"], "ratunek": 30}

from collections import Counter
from itertools import combinations, combinations_with_replacement
from scipy.stats import binom
import json
import random
import pandas as pd
import score
import numpy as np
import matplotlib.pyplot as plt


def read_move_dict():
    """
    Read dictionary with results from generate_moves.py.
    """

    with open("moves.json", "r") as read_file:
        data = json.load(read_file)

    return {key: pd.read_json(data[key]) for key in data}


def best_moves(throw, move_dict, prioritize='score', rarity_coef=13, log=False):
    """
    Recalculate best move for provided throw, given a provided routine. Default: the one that
    seemed to score the best on average, where used to play a full game.
    """

    moves = move_dict[str(tuple(throw))]
    if log:
        moves.score = np.log(moves.gain + 1e-7) * (moves.rarity) ** rarity_coef
    else:
        moves.score = moves.gain * (moves.rarity) ** rarity_coef
    return round(moves.sort_values(by=prioritize, ascending=False), 2)


def play_full_turn(game_sheet, move_dict, prioritize='score', throws=3, rarity_coef=13, log=False):
    """
    Plays a full turn with 3 throws, to the best of its capabilities. Writes the final throw into
    the game_sheet.
    """

    current_throw = random.choices(range(1, 7), k=5)
    current_throw.sort()

    for _ in range(throws-1):
        moves = best_moves(current_throw, move_dict, prioritize=prioritize,
                           rarity_coef=rarity_coef, log=log)
        mask = [el not in game_sheet for el in moves.index]

        figure = moves[mask].index[0]
        best_move = eval(moves[mask]['to keep'].iloc[0])
        current_throw = list(best_move) + random.choices(range(1, 7), k=5-len(best_move))
        current_throw.sort()

    game_sheet[figure] = current_throw
    return game_sheet


def play_game(move_dict, prioritize='score', rarity_coef=13, log=False):
    """
    Plays the whole game of Yahtzee, return a game_sheet with every final throw.
    """

    game_sheet = {}

    for _ in range(15):
        game_sheet = play_full_turn(game_sheet, move_dict, prioritize=prioritize,
                                    rarity_coef=rarity_coef, log=log)

    return game_sheet


def score_sheet(game_sheet):
    """
    For every final throw in a game_sheet, calculate its score and return the total score from every
    turn.
    """

    game_sheet = {key: Counter(game_sheet[key]) for key in game_sheet}
    scores = {}

    scores["1"] = score.gorna(1, game_sheet["1"])
    scores["2"] = score.gorna(2, game_sheet["2"])
    scores["3"] = score.gorna(3, game_sheet["3"])
    scores["4"] = score.gorna(4, game_sheet["4"])
    scores["5"] = score.gorna(5, game_sheet["5"])
    scores["6"] = score.gorna(6, game_sheet["6"])
    scores["para"] = score.para(game_sheet["para"])
    scores["dwie pary"] = score.dpary(game_sheet["dwie pary"])
    scores["trojka"] = score.trojka(game_sheet["trojka"])
    scores["maly strit"] = score.maly_strit(game_sheet["maly strit"])
    scores["duzy strit"] = score.duzy_strit(game_sheet["duzy strit"])
    scores["full"] = score.full(game_sheet["full"])
    scores["kareta"] = score.kareta(game_sheet["kareta"])
    scores["general"] = score.general(game_sheet["general"])
    scores["ratunek"] = score.ratunek(game_sheet["ratunek"])

    total = 0
    for key in scores:
        total += scores[key]

    return total


def check_avg_score(prioritize='score', rarity_coef=13, n=1000, log=False):
    """
    Check average score from n full games with a provided routine.
    """

    scores = []
    for _ in range(n):
        game_sheet = play_game(move_dict, rarity_coef=rarity_coef, log=log)
        scores.append(score_sheet(game_sheet))
    return np.mean(scores)


move_dict = read_move_dict()
best_moves([1, 1, 2, 2, 6], move_dict)

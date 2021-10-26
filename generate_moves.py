from collections import Counter
from itertools import combinations, combinations_with_replacement
from scipy.stats import binom
import json
import random
import pandas as pd
import score


def choose_best_moves(roll, n=1000):
    """
    For every way to preserve some part of the roll, reroll removed dice n times. Score every roll
    for each figure, then choose the best move for each figure based on average from n tries.

    Return dataframe with results, sorted by score - expected score (based on what you could expect
    from rerolling every dice).
    """

    df = pd.DataFrame()
    for i in range(6):
        for keep in combinations(roll, i):
            df = df.append(pd.DataFrame(score.get_average(keep, n), index=[str(keep)]))
    dfref = {"average": df.loc["()"], "max": pd.Series(score.get_max())}

    to_print = pd.DataFrame()
    for column in df.columns:
        new_row = {"to keep": df.loc[:, column].idxmax(), "value": round(df.loc[:, column].max(), 2),
                   "gain": round(df.loc[:, column].max() - dfref["average"][column], 2)}
        new_row["%gain"] = round(new_row["gain"] / (dfref["max"][column] - dfref["average"][column]), 2) * 100
        new_row = pd.DataFrame(new_row, index=[column])
        to_print = to_print.append(new_row)

    return to_print.sort_values(["gain"], ascending=False)


def generate_move_dict(n=10000, save_to='moves.json'):
    """
    For all possible 5-rolls, classify all figures and their best moves based on n tries.
    Dump dictionary with results into a .json file.
    """

    dict = {}
    for comb in combinations_with_replacement([1, 2, 3, 4, 5, 6], 5):
        dict[str(comb)] = choose_best_moves(comb, n)
    dict = calculate_rarity(dict)
    for comb in dict.keys():
        dict[comb] = dict[comb].to_json()

    with open(save_to, 'w') as fp:
        json.dump(dict, fp)


def calculate_rarity(all_combs):
    """
    Calculate rarity - i.e. how rare for a roll it is to have the same or better expected score.
    Append the rarity to the dataframe.
    """

    all_figures = {}
    for figure in all_combs[list(all_combs.keys())[0]].index:
        values = {}
        for comb in all_combs.keys():
            values[comb] = round(all_combs[comb].loc[figure, 'gain'], 1)
        values = pd.DataFrame(pd.Series(values), columns=['gain']).sort_values(by='gain')
        values.index.name = 'combination'
        values = values.reset_index()

        prob_not_better = pd.Series([0 for i in range(len(values))], dtype='float64')
        for i in range(len(values)):
            prob_not_better[i] = sum(values['gain'] < values.loc[i, 'gain'] + 0.1)/len(values)
        values['rarity'] = prob_not_better
        values = values.set_index('combination')

        all_figures[figure] = values

    for comb in all_combs.keys():
        rarity = [all_figures[figure].loc[comb, 'rarity'] for figure in all_combs[comb].index]
        rarity = pd.Series(rarity, index=all_combs[comb].index)
        all_combs[comb]['rarity'] = rarity
        all_combs[comb]['score'] = all_combs[comb]['gain'] * all_combs[comb]['rarity']
        all_combs[comb] = all_combs[comb].sort_values(by='score', ascending=False)

    return all_combs


generate_move_dict(20000)

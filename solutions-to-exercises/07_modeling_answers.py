"""
Answers to the end of chapter exercises for Modeling chapter.
"""
import pandas as pd
import random
from pandas import DataFrame, Series
import statsmodels.formula.api as smf
from os import path

DATA_DIR = './data'

###############################################################################
# problem 7.1
###############################################################################

###################
# from 07_01_ols.py
###################
df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

df['dist_sq'] = df['dist']**2
df['made'] = df['made'].astype(int)

df[['made', 'dist', 'dist_sq']].head()

model = smf.ols(formula='made ~ dist + dist_sq', data=df)
results = model.fit()

results.summary2()

def prob_of_make(dist):
    b0, b1, b2 = results.params
    return (b0 + b1*dist + b2*(dist**2))

df['made_hat'] = results.predict(df)

#########################
# answers to question 7.1
#########################
# a
df['made_hat_alt'] = df['dist'].apply(prob_of_make)

df[['made_hat', 'made_hat_alt']].head()

# check whether made_hat and made_hat_alt are within some epsilon

(df['made_hat_alt'] == df['made_hat']).all()

import numpy as np
(np.abs(df['made_hat'] - df['made_hat_alt']) < .00000001).all()

# b
model_b = smf.ols(
    formula='made ~ dist + dist_sq + C(value)', data=df)
results_b = model_b.fit()
results_b.summary2()

# c
df['is3'] = df['value'] == 3

model_d = smf.ols(formula='made ~ dist + dist_sq + is3', data=df)
results_d = model_d.fit()
results_d.summary2()

###############################################################################
# problem 7.2
###############################################################################

# a
def run_sim_get_pvalue():
    coin = ['H', 'T']

    # make empty DataFrame
    df = DataFrame(index=range(100))

    # now fill it with a "guess"
    df['guess'] = [random.choice(coin) for _ in range(100)]

    # and flip
    df['result'] = [random.choice(coin) for _ in range(100)]

    # did we get it right or not?
    df['right'] = (df['guess'] == df['result']).astype(int)

    model = smf.ols(formula='right ~ C(guess)', data=df)
    results = model.fit()

    return results.pvalues['C(guess)[T.T]']

# b
sims_1k = Series([run_sim_get_pvalue() for _ in range(1000)])
sims_1k.mean()  # 0.5083

# c
def runs_till_threshold(i, p=0.05):
    pvalue = run_sim_get_pvalue()
    if pvalue < p:
        return i
    else:
        return runs_till_threshold(i+1, p)

sim_time_till_sig_100 = Series([runs_till_threshold(1) for _ in range(100)])

# d

# According to Wikipedia, the mean and median of the Geometric distribution are
# 1/p and -1/log_2(1-p). Since we're working with a p of 0.05, that'd give us:

from math import log
p = 0.05
g_mean = 1/p  # 20
g_median = -1/log(1-p, 2)  # 13.51

g_mean, g_median

sim_time_till_sig_100.mean()
sim_time_till_sig_100.median()

###############################################################################
# problem 7.3
###############################################################################

dftg = pd.read_csv(path.join(DATA_DIR, 'team_games.csv'))

# a) Run a logit model regressing three point percentage, offensive and defensive
#    rebounds, steals, turnovers and blocks on whether a team wins.

dftg['win'] = (dftg['wl'] == 'W').astype(int)

# a
model_a = smf.logit(formula=
                    """
                    win ~ fg3_pct + oreb + dreb + stl + tov + blk
                    """, data=dftg)
results_a = model_a.fit()
results_a.summary2()

margeff = results_a.get_margeff()
margeff.summary()

# b
model_b = smf.logit(formula=
                    """
                    win ~ fg3_pct + oreb + dreb + stl + tov + blk + C(team)
                    """, data=dftg)
results_b = model_b.fit()
results_b.summary2()

###############################################################################
# problem 7.4
###############################################################################
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score

xvars = ['min', 'pts', 'fgm', 'fga', 'fg_pct', 'fg3m', 'fg3a', 'fg3_pct',
    'ftm', 'fta', 'ft_pct', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'tov',
    'pf', 'plus_minus', 'bubble', 'win']

yvar = 'team'

model = RandomForestClassifier(n_estimators=100)

scores = cross_val_score(model, dftg[xvars], dftg[yvar], cv=10)
scores.mean()  
scores.min()
scores.max()

# d
1/30  # .033 with random guess

# feature important on model
model.fit(dftg[xvars], dftg[yvar])  # running model fitting on entire dataset
Series(model.feature_importances_, xvars).sort_values(ascending=False)

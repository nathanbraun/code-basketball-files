import pandas as pd
import numpy as np
from patsy import dmatrices
from pandas import DataFrame, Series
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from os import path

DATA_DIR = './data'

df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

######################################################
# processing - included extra comments to follow along
######################################################

# time left in quarter - decimal format
df['time_left'] = df['min_left'] + df['sec_left']/60

# we'll be categorizing shot type - currently in series of dummy columns
# types to look at:
shot_types = ['layup', 'pullup', 'float', 'dunk', 'hook', 'fadeaway']

# plan:
# 1. create catch-all, "other" type that is NOT one of the above
# 2. then go through and make new variable shot_type that is either layup,
# pullup, etc or other

# catch all other variable
df['other'] = df[shot_types].sum(axis=1) == 0

# create shot type variable
df['shot_type'] = 'other'
for shot in shot_types:
    df.loc[df[shot], 'shot_type'] = shot
    
# book picks up here
xvars = ['dist', 'x', 'y', 'period', 'time_left']
yvar = 'shot_type'

df[xvars + [yvar]].sample(10)

df[yvar].value_counts(normalize=True)

# holdout set
train, test = train_test_split(df, test_size=0.20)

model = RandomForestClassifier(n_estimators=100)
model.fit(train[xvars], train[yvar])

test['shot_type_hat'] = model.predict(test[xvars])

test['correct'] = (test['shot_type_hat'] == test['shot_type'])
test['correct'].mean()

model.predict_proba(test[xvars])

probs = DataFrame(model.predict_proba(test[xvars]),
                  index=test.index,
                  columns=model.classes_)

probs.head()

results = pd.concat([test[['name', 'dist', 'shot_type', 'shot_type_hat',
    'correct']], probs], axis=1)

results.groupby('shot_type')[['correct', 'layup', 'pullup', 'float', 'dunk',
    'hook', 'fadeaway', 'other']].mean().round(2)

# cross validation
model = RandomForestClassifier(n_estimators=100)

# note: cross validation takes a minute to run, if you're on an old computer
# try changing cv to 5 or 3
scores = cross_val_score(model, df[xvars], df[yvar], cv=10)

scores
scores.mean()

# feature importance
model = RandomForestClassifier(n_estimators=100)
model.fit(df[xvars], df[yvar])

Series(model.feature_importances_, xvars).sort_values(ascending=False)


dfs = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))
dfp = pd.read_csv(path.join(DATA_DIR, 'players.csv'))
dfg = pd.read_csv(path.join(DATA_DIR, 'games.csv'))
dfpg = pd.read_csv(path.join(DATA_DIR, 'player_game.csv'))
dfb = pd.read_csv(path.join(DATA_DIR, 'box_adv.csv'))
dft = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))
dftg = pd.read_csv(path.join(DATA_DIR, 'team_games.csv'))

#########################
# predicting wins example
#########################
Index(['game_id', 'home', 'away', 'date', 'home_pts', 'away_pts', 'min',
       'home_fgm', 'home_fga', 'home_fg_pct', 'home_fg3m', 'home_fg3a',
       'home_fg3_pct', 'home_ftm', 'home_fta', 'home_ft_pct', 'home_oreb',
       'home_dreb', 'home_reb', 'home_ast', 'home_stl', 'home_blk', 'home_tov',
       'home_pf', 'home_plus_minus', 'away_fgm', 'away_fga', 'away_fg_pct',
       'away_fg3m', 'away_fg3a', 'away_fg3_pct', 'away_ftm', 'away_fta',
       'away_ft_pct', 'away_oreb', 'away_dreb', 'away_reb', 'away_ast',
       'away_stl', 'away_blk', 'away_tov', 'away_pf', 'away_plus_minus',
       'bubble', 'sample', 'season'],
      dtype='object')

cols = ['home', 'away', 'home_pts', 'away_pts', 'home_fgm', 'home_fga',
        'home_fg_pct', 'home_fg3m', 'home_fg3a', 'home_fg3_pct', 'home_ftm',
        'home_fta', 'home_ft_pct', 'home_oreb', 'home_dreb', 'home_reb',
        'home_ast', 'home_stl', 'home_blk', 'home_tov', 'home_pf',
        'home_plus_minus', 'away_fgm', 'away_fga', 'away_fg_pct', 'away_fg3m',
        'away_fg3a', 'away_fg3_pct', 'away_ftm', 'away_fta', 'away_ft_pct',
        'away_oreb', 'away_dreb', 'away_reb', 'away_ast', 'away_stl',
        'away_blk', 'away_tov', 'away_pf', 'away_plus_minus']

# includes
# selecting and renaming columns, concatenating, grouping

dfh = DataFrame(dfg[cols], copy=True)
dfh['win'] = dfh['home_pts'] > dfh['away_pts']
dfh.columns = [x.replace('home', 'team') for x in dfh.columns]
dfh.columns = [x.replace('away', 'opp') for x in dfh.columns]

dfa = DataFrame(dfg[cols], copy=True)
dfa['win'] = dfa['home_pts'] < dfa['away_pts']
dfa.columns = [x.replace('away', 'team') for x in dfa.columns]
dfa.columns = [x.replace('home', 'opp') for x in dfa.columns]

df = pd.concat([dfh, dfa], ignore_index=True)

sum_cols = ['team_pts', 'opp_pts', 'team_fgm', 'team_fga', 'team_fg3m',
        'team_fg3a', 'team_ftm', 'team_fta', 'team_oreb', 'team_dreb',
        'team_reb', 'team_ast', 'team_stl', 'team_blk', 'team_tov', 'team_pf',
        'team_plus_minus', 'opp_fgm', 'opp_fga', 'opp_fg3m', 'opp_fg3a',
        'opp_ftm', 'opp_fta', 'opp_oreb', 'opp_dreb', 'opp_reb', 'opp_ast',
        'opp_stl', 'opp_blk', 'opp_tov', 'opp_pf', 'opp_plus_minus', 'win']

df2 = df.groupby('team')[sum_cols].sum().reset_index()

xvars = ['team_pts', 'opp_pts', 'team_fgm', 'team_fga', 'team_fg3m',
        'team_fg3a', 'team_ftm', 'team_fta', 'team_oreb', 'team_dreb',
        'team_reb', 'team_ast', 'team_stl', 'team_blk', 'team_tov', 'team_pf',
        'opp_fgm', 'opp_fga', 'opp_fg3m', 'opp_fg3a',
        'opp_ftm', 'opp_fta', 'opp_oreb', 'opp_dreb', 'opp_reb', 'opp_ast',
        'opp_stl', 'opp_blk', 'opp_tov', 'opp_pf']
yvar = 'team'

train, test = train_test_split(df, test_size=0.20)

model = RandomForestClassifier(n_estimators=100)
model.fit(train[xvars], train[yvar])

test['team_hat'] = model.predict(test[xvars])
test['correct'] = (test['team_hat'] == test['team'])
test['correct'].mean()

probs = DataFrame(model.predict_proba(test[xvars]),
                  index=test.index,
                  columns=model.classes_)
probs.head()

probs['actual'] = test['team']

model.fit(df2[xvars], df2[yvar])  # running model fitting on entire dataset
Series(model.feature_importances_, xvars).sort_values(ascending=False)

################################################
# original example - predicting made or not made
################################################

cats2 = ['layup', 'pullup', 'float', 'dunk', 'hook', 'fadeaway', 'step']
dfs['basic'] = dfs[cats2].sum(axis=1) == 0

dfs['shot_type'] = np.nan
for shot in cats2 + ['basic']:
    dfs.loc[dfs[shot], 'shot_type'] = shot
    
dfs['time_left'] = dfs['min_left'] + dfs['sec_left']/60

# try shot type example
xvars = ['dist', 'x', 'y', 'period', 'time_left']
yvar = 'shot_type'

train, test = train_test_split(dfs, test_size=0.20)

model = RandomForestClassifier(n_estimators=100)
model.fit(train[xvars], train[yvar])

test['shot_type_hat'] = model.predict(test[xvars])
test['correct'] = (test['shot_type_hat'] == test['shot_type'])
test['correct'].mean()

model.predict_proba(test[xvars])

probs = DataFrame(model.predict_proba(test[xvars]),
                  index=test.index,
                  columns=model.classes_)

probs.head()

probs[['actual', 'correct']] = test[['shot_type', 'correct']]

probs.head()

probs.groupby('actual')[['correct', 'layup', 'pullup', 'float', 'dunk',
    'hook', 'fadeaway', 'step', 'basic']].mean().round(2)

# cross validation
model = RandomForestClassifier(n_estimators=100)
scores = cross_val_score(model, dfs[xvars], dfs[yvar], cv=10)

scores
scores.mean()

model = RandomForestClassifier(n_estimators=100)
model.fit(dfs[xvars], dfs[yvar])

Series(model.feature_importances_, xvars).sort_values(ascending=False)

# then add in player info - height, weight, year entered the league

height = '6-6'
height = height.split('-')
ft = height[0]
inches = height[1]
height_dec = int(ft) + int(inches)/12

def height_to_dec(height):
    height = height.split('-')
    ft = height[0]
    inches = height[1]
    return int(ft) + int(inches)/12

dfp['height_dec'] = dfp['height'].apply(height_to_dec)

dfs2 = pd.merge(dfs, dfp[['player_id', 'height_dec', 'weight', 'from_year']],
        how='left')

xvars = ['ln_dist', 'x', 'y', 'period', 'min_left', 'sec_left', 'height_dec',
        'weight', 'from_year']
yvar = 'shot_type'

train, test = train_test_split(dfs2, test_size=0.20)

model = RandomForestClassifier(n_estimators=100)
model.fit(train[xvars], train[yvar])

test['shot_hat'] = model.predict(test[xvars])
test['correct'] = (test['shot_hat'] == test['shot_type'])
test['correct'].mean()

# probs.columns = ['pmiss', 'pmake']

# original

dfs['ln_dist'] = np.log(dfs['dist'].apply(lambda x: max(x, 0.5)))

xvars = ['ln_dist', 'value', 'x', 'y', 'running', 'jump', 'hook', 'layup',
         'driving', 'dunk', 'alley', 'reverse', 'turnaround', 'fadeaway',
         'bank', 'finger', 'putback', 'float', 'pullup', 'step', 'cutting',
         'tip', 'period', 'min_left', 'sec_left']

yvar = 'made'

train, test = train_test_split(dfs, test_size=0.20)

model = RandomForestClassifier(n_estimators=100)
model.fit(train[xvars], train[yvar])

test['made_hat'] = model.predict(test[xvars])
test['correct'] = (test['made_hat'] == test['made'])
test['correct'].mean()

model.predict_proba(test[xvars])

probs = DataFrame(model.predict_proba(test[xvars]),
                  index=test.index,
                  columns=model.classes_)
probs.head()
probs.columns = ['pmiss', 'pmake']

results = pd.concat([
    test[['name', 'shot_id', 'shot_type', 'dist', 'made', 'made_hat',
          'correct']],
    probs[['pmake']]], axis=1)


results.sample(5)

results.groupby(['shot_type', 'made'])['correct'].mean().to_frame().unstack()

results['pmake_bin'] = pd.cut(results['pmake'], 10)

results.groupby('pmake_bin')['made'].mean()

# cross validation
model = RandomForestClassifier(n_estimators=100)
scores = cross_val_score(model, dfs[xvars], dfs[yvar], cv=10)

scores
scores.mean()

# feature importance
model.fit(dfs[xvars], dfs[yvar])  # running model fitting on entire dataset
Series(model.feature_importances_, xvars).sort_values(ascending=False)

# homework: add in some player info?

# vs logit model
dfs['ln_dist'] = np.log(dfs['dist'].apply(lambda x: max(x, 0.5)))
dfs['made'] = dfs['made'].astype(int)
y, X = dmatrices('made ~ dist', dfs)

model = LogisticRegression()
scores = cross_val_score(model, X, y, cv=10)

scores
scores.mean()

# more

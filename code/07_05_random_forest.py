import pandas as pd
from patsy import dmatrices
from pandas import DataFrame, Series
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from os import path

DATA_DIR = '/Users/nathanbraun/fantasymath/basketball/nba_api/data'

dfs = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

cats2 = ['layup', 'pullup', 'float', 'dunk', 'hook', 'fadeaway', 'step']
dfs['basic'] = dfs[cats2].sum(axis=1) == 0

dfs['shot_type'] = np.nan
for shot in cats2 + ['basic']:
    dfs.loc[dfs[shot], 'shot_type'] = shot

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

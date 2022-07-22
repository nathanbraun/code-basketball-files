import pandas as pd
import numpy as np
import math
from textwrap import dedent
import statsmodels.formula.api as smf
from os import path

DATA_DIR = './data'

df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

cats2 = ['layup', 'pullup', 'float', 'dunk', 'hook', 'fadeaway', 'step']
df['basic'] = df[cats2].sum(axis=1) == 0
df['dist_sq'] = df['dist'] ** 2

df['shot_type'] = np.nan
for shot in cats2 + ['basic']:
    df.loc[df[shot], 'shot_type'] = shot

df['made'] = df['made'].astype(int)

#########################
# holding things constant
#########################

# dunk: increases prob of making shot by 0.48
model = smf.ols(formula=
        """
        made ~ dunk
        """, data=df)
results = model.fit()
results.summary2()

df.groupby('dunk')['dist'].mean()

# fine but dunks close
model = smf.ols(formula=
        """
        made ~ dunk + dist
        """, data=df)
results = model.fit()
results.summary2()

# let's add layup
model = smf.ols(formula=
        """
        made ~ dunk + dist + layup
        """, data=df)
results = model.fit()
results.summary2()


0.4913 -0.0055*18.5

0.4913 -0.0055*1 + 0.4273
0.4913 -0.0055*2 + 0.0669

# interesting stuff with dist too

cats = ['jump', 'hook', 'layup', 'driving', 'dunk', 'alley', 'reverse',
        'turnaround', 'fadeaway', 'bank', 'finger', 'putback', 'float',
        'pullup', 'step', 'cutting', 'tip']

df['ncats'] = df[cats].sum(axis=1)

###############
# fixed effects
###############
pd.get_dummies(df['shot_type']).head()

model = smf.ols(formula="made ~ C(shot_type) + dist + dist_sq", data=df)
results = model.fit()
results.summary2()

model = smf.ols(
    formula="made ~ C(shot_type, Treatment(reference='layup')) + dist + dist_sq", data=df)
results = model.fit()
results.summary2()

b0 = 0.5715
b_dist = -0.0135
b_dist2 = 0.0001

b0 + b_dist*25 + b_dist2*(25^2) + 0.0483

b0 + b_dist*15 + b_dist2*(15^2) + 0.0212

b0 + b_dist*3 + b_dist2*(3^2)

####################
# squaring variables
####################

df['dist2'] = df['dist'] ** 2
model = smf.ols(formula="made ~ dist + dist2", data=df)
results = model.fit()
results.summary2()

# cubed variables
df['dist3'] = df['dist'] ** 3
model = smf.ols(formula="made ~ dist + dist2 + dist3", data=df)
results = model.fit()
results.summary2()

#############
# natural log
#############
df['ln_dist'] = np.log(df['dist'].apply(lambda x: max(x, 0.5)))

model = smf.ols(formula='made ~ ln_dist', data=df)
results = model.fit()
results.summary2()

#############
# intractions
#############
df['is_layup'] = df['shot_type'] == 'layup'

model = smf.ols(formula=
        """
        made ~ dist + dist:is_layup
        """, data=df)
results = model.fit()
results.summary2()


model = smf.ols(formula=
        """
        made ~ C(shot_type) + dist + dist:layup
        """, data=df)
results = model.fit()
results.summary2()

model = smf.ols(formula=
        """
        made ~ C(shot_type)*ln_dist
        """, data=df)
results = model.fit()
results.summary2()

#######
# logit
#######
model = smf.logit(formula=
        """
        made ~ layup + dist + dist:layup
        """, data=df)
logit_results = model.fit()
logit_results.summary2()

def prob_made_logit(dist, is_layup):
    b0, b1, b2, b3 = logit_results.params
    value = (b0 + b1*is_layup + b2*dist + b3*is_layup*dist)
    return 1/(1 + math.exp(-value))

prob_made_logit(0, 1)
prob_made_logit(15, 0)
prob_made_logit(2, 1)

# have to look at range too
prob_made(80, 0, 0)


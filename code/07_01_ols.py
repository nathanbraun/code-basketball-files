import pandas as pd
import statsmodels.formula.api as smf
from os import path

DATA_DIR = '/Users/nathanbraun/fantasymath/basketball/nba_api/data'

###################
# linear regression
###################

# load
df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

df['dist_sq'] = df['dist']**2
df['made'] = df['made'].astype(int)

df[['made', 'dist', 'dist_sq']].head()

model = smf.ols(formula='made ~ dist + dist_sq', data=df)
results = model.fit()

results.summary2()

def prob_of_make(yds):
    b0, b1, b2 = results.params
    return (b0 + b1*yds + b2*(yds**2))

prob_of_make(1)
prob_of_make(25)
prob_of_make(30)

# process

df['made_hat'] = results.predict(df)
df[['made', 'made_hat']].head(10)


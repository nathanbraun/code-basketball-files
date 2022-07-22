import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from os import path
import random

pd.options.mode.chained_assignment = None
%matplotlib qt

# directories
DATA_DIR = './data'

# load data
dfs = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))  
dfg = pd.read_csv(path.join(DATA_DIR, 'games.csv'))  
dft = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))
dftg = pd.read_csv(path.join(DATA_DIR, 'team_games.csv'))

# process data
cats2 = ['layup', 'pullup', 'float', 'dunk', 'hook', 'fadeaway', 'step']
dfs['jump'] = dfs[cats2].sum(axis=1) == 0

dfs['shot_type'] = np.nan
for shot in cats2 + ['jump']:
    dfs.loc[dfs[shot], 'shot_type'] = shot

dfg.rename(columns={'home': 'home_team', 'away': 'away_team'}, inplace=True)

# book picks up here:

###############
# summary stats
###############

# quantile function and describe

dfs['dist'].quantile(.9)
dfs[['dist', 'value']].describe()

# % of shots 0-9 feet
dfs['dist'].value_counts(normalize=True).sort_index().head(10)

##########
# plotting
##########

# basic displot
# all on one line
g = sns.FacetGrid(dfs).map(sns.kdeplot, 'dist', shade=True)

# on seperate lines so it's clearer it's a two step process
g = (sns.FacetGrid(dfs)
     .map(sns.kdeplot, 'dist', shade=True))

# invert axis
g = (sns.FacetGrid(dfs)
     .map(sns.kdeplot, 'dist', shade=True))
g.set(xlim=(-5, 40))
g.ax.invert_xaxis()

# density plot by shot type + made
g = sns.displot(dfs, x='dist', kind='kde', hue='shot_type', fill=True)
g.set(xlim=(-5, 40))
g.ax.invert_xaxis()
plt.show()

# too spiky, let's jitter it
import random
random.uniform(0, 1)

[random.gauss(0, 1) for _ in range(10)]

dfs['jdist'] = dfs['dist']
dfs.loc[dfs['shot_type'] == 'layup', 'jdist'] = dfs['dist'].apply(lambda x: x +
        random.gauss(0, 1))
dfs.loc[dfs['shot_type'] == 'dunk', 'jdist'] = dfs['dist'].apply(lambda x: x +
        random.gauss(0, 1))

g = (sns.FacetGrid(dfs, hue='shot_type')
     .map(sns.kdeplot, 'jdist', shade=True))
g.set(xlim=(-5, 40))
[ax[0].invert_xaxis() for ax in g.axes]
g.add_legend()
plt.show()

g = (sns.FacetGrid(dfs, hue='shot_type', col='made')
     .map(sns.kdeplot, 'jdist', shade=True))
g.set(xlim=(-5, 40))
[ax[0].invert_xaxis() for ax in g.axes]
g.add_legend()
plt.show()

# swap hue, col
g = (sns.FacetGrid(dfs, col='shot_type', hue='made', col_wrap=3)
     .map(sns.kdeplot, 'jdist', shade=True))
g.set(xlim=(-5, 40))
[ax.invert_xaxis() for ax in g.axes]
g.add_legend()
plt.show()

# lessons: matters, esp for hook shots; not as much for jumper

#########################
# processing for plotting
#########################

# example of reshaping data to get it into the shape we want

# thinking about seaborn: specify seperate columns for columns, hue (color),
# thing we're plotting (points)
# so we need points in one column, then another type for scoring type

# book picks up again here:
dfg[['date', 'home_team', 'away_team', 'home_pts', 'away_pts']].head()

def home_away_pts_df(df, location):
    df = df[['date', f'{location}_team', f'{location}_pts']]
    df.columns = ['date', 'team', 'pts']
    df['location'] = location
    return df

home_away_pts_df(dfg, 'home').head()

pts_long = pd.concat([
    home_away_pts_df(dfg, loc) for loc in ['home', 'away']], ignore_index=True)

# now can plot points by scoring system and position
g = (sns.FacetGrid(pts_long, hue='location')
     .map(sns.kdeplot, 'pts', shade=True))
g.add_legend()
plt.show()

# now extend it to ALL columns

location = 'home'
opp = 'away'

team_cols = [x for x in dfg.columns if x.startswith(location)]
team_cols

opp_cols = [x for x in dfg.columns if x.startswith(opp)]
opp_cols

df_team = dfg[team_cols]
df_team.columns = [x.replace(f'{location}_', '') for x in df_team.columns]
df_team.head()

df_opp = dfg[opp_cols]
df_opp.columns = [x.replace(opp, 'opp') for x in df_opp.columns]
df_opp.head()

dfg_wide = pd.concat([df_team, df_opp], axis=1)
dfg_wide.head()

def home_away_all(df, location):
    if location == 'home':
        opp = 'away'
    elif location == 'away':
        opp = 'home'

    team_cols = [x for x in df.columns if x.startswith(location)]
    team_cols

    opp_cols = [x for x in df.columns if x.startswith(opp)]
    opp_cols

    df_team = df[team_cols]
    df_team.columns = [x.replace(f'{location}_', '') for x in df_team.columns]
    df_team.head()

    df_opp = df[opp_cols]
    df_opp.columns = [x.replace(opp, 'opp') for x in df_opp.columns]
    df_opp.head()

    return pd.concat([df_team, df_opp], axis=1)

dfg_wide = pd.concat([
    home_away_all(dfg, 'home'),
    home_away_all(dfg, 'away')])

other_cols = [x for x in dfg.columns
               if not ((x.startswith('home')) or (x.startswith('away')))]
other_cols

df_all = pd.concat([dfg_wide, dfg[other_cols]], axis=1)
df_all['win'] = dfg_wide['pts'] > dfg_wide['opp_pts']

df_all.head()

# now we can do things like look at scoring by team/bubble
g = (sns.FacetGrid(df_all, hue='bubble', col='team', col_wrap=5)
     .map(sns.kdeplot, 'pts', shade=True))
g.add_legend()

#################################
# relationships between variables
#################################

# fg pct vs pts
sns.relplot(x='fg_pct', y='pts', data=df_all)
plt.show()

# fg pct vs pts - win/loss
sns.relplot(x='fg_pct', y='pts', hue='win', data=df_all)
plt.show()

# fg pct vs pts - win/loss - by team
sns.relplot(x='fg3_pct', y='pts', col='team', hue='win', col_wrap=5, data=df_all)
g.add_legend()
plt.show()

#############
# correlation
#############

df_all[['pts', 'reb', 'win', 'fg3_pct', 'fgm', 'blk', 'opp_fg3_pct']].corr().round(2)

# scatter plot of 0.43 correlation
g = sns.relplot(x='fg3_pct', y='fgm', data=df_all)
plt.show()

# scatter plot of -0.33 correlation
g = sns.relplot(x='opp_fg3_pct', y='reb', data=df_all)
plt.show()

# scatter plot of 0.83 correlation
g = sns.relplot(x='fgm', y='pts', data=df_all)
plt.show()

########################
# line plots with python
########################

df_all = pd.merge(df_all, dft[['team', 'division', 'conference']])

# book picks back up here
df_all['month'] = df_all['date'].str[5:7].astype(int)

g = sns.relplot(x='month', y='pts', kind='line', data=df_all.query("~bubble"),
                hue='conference')
plt.show()

df_all.loc[(df_all['month'] == 11) & (df_all['conference'] == 'East'), ['date',
    'team', 'opp_team', 'pts', 'opp_pts', 'conference']].sort_values('date').head()

# max points by month and conference
max_pts = (df_all.query("~bubble").groupby(['conference', 'month'], as_index=False)['pts'].max())

g = sns.relplot(x='month', y='pts', kind='line', style='conference',
        data=max_pts, hue='conference')
plt.show()

##############
# plot options
##############

# basic plot
g = (sns.FacetGrid(dfs, col='shot_type', hue='made')
     .map(sns.kdeplot, 'dist', shade=True))

# wrap columns
g = (sns.FacetGrid(dfs, col='shot_type', hue='made', col_wrap=3)
     .map(sns.kdeplot, 'dist', shade=True))

# adding a title
g.fig.subplots_adjust(top=0.9) # adding a title
g.fig.suptitle('Distribution of Shot Distances by Type, Made')

# modifying options
g.set(xlim=(-5, 40))

g.set_xlabels('Ft')
g.set_ylabels('Density')

# saving
g.savefig('shot_dist_type_made.png')


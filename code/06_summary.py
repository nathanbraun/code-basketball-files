import pandas as pd
import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = '/Users/nathanbraun/fantasymath/basketball/nba_api/data'
FIG_DIR = '/Users/nathanbraun/fantasymath/basketball/nba_api/fig'

# load data
df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

###############
# summary stats
###############

# book picks up here:

# quantile function and describe

df['dist'].quantile(.9)
df[['dist', 'value']].describe()

##########
# plotting
##########

# basic displot
g = (sns.FacetGrid(df)
     .map(sns.kdeplot, 'dist', shade=True))
g.set(xlim=(-5, 40))


# TODO: add this to data earlier
cats2 = ['layup', 'pullup', 'float', 'dunk', 'hook', 'fadeaway', 'step']
df['jump'] = df[cats2].sum(axis=1) == 0

df['shot_type'] = np.nan
for shot in cats2 + ['jump']:
    df.loc[df[shot], 'shot_type'] = shot

# density plot by shot type + made
g = sns.displot(df, x='dist', kind='kde', hue='shot_type', fill=True)
plt.show()

g = (sns.FacetGrid(df, hue='shot_type')
     .map(sns.kdeplot, 'dist', shade=True))
g.set(xlim=(-5, 40))
plt.show()

g = (sns.FacetGrid(df, hue='shot_type', col='made')
     .map(sns.kdeplot, 'dist', shade=True))
g.set(xlim=(-5, 40))
plt.show()

# swap hue, col
g = (sns.FacetGrid(df, col='shot_type', hue='made', col_wrap=3)
     .map(sns.kdeplot, 'dist', shade=True))
g.set(xlim=(-5, 40))
plt.show()

# lessons: hook shot dist matters

#########################
# processing for plotting
#########################

# example of reshaping data to get it into the shape we want

# thinking about seaborn: specify seperate columns for columns, hue (color),
# thing we're plotting (points)
# so we need points in one column, then another type for scoring type

# do with team/game data
games = pd.read_csv(path.join(DATA_DIR, 'games.csv'))
games.rename(columns={'home': 'home_team', 'away': 'away_team'}, inplace=True)

# book picks up again here:
games[['home_team', 'away_team', 'home_pts', 'away_pts']].head()

def home_away_pts_df(_df, location):
    _df = _df[['date', f'{location}_team', f'{location}_pts']]
    _df.columns = ['date', 'team', 'pts']
    _df['location'] = location
    return _df

home_away_pts_df(games, 'home').head()

pts_long = pd.concat([
    home_away_pts_df(games, loc) for loc in ['home', 'away']], ignore_index=True)

# now can plot points by scoring system and position
g = (sns.FacetGrid(pts_long, hue='location')
     .map(sns.kdeplot, 'pts', shade=True))
g.add_legend()
plt.show()

# now extend it to ALL columns

location = 'home'
opp = 'away'

team_cols = [x for x in games.columns if x.startswith(location)]
opp_cols = [x for x in games.columns if x.startswith(opp)]

df_team = games[team_cols]
df_team.columns = [x.replace(f'{location}_', '') for x in df_team.columns]

df_opp = games[opp_cols]
df_opp.columns = [x.replace(opp, 'opp') for x in df_opp.columns]

common_cols = [x for x in games.columns
               if not ((x.startswith('home')) or (x.startswith('away')))]

df_all = pd.concat([games[common_cols], df_team, df_opp], axis=1)

def games_to_team(df_wide, location):
    if location == 'home':
        opp = 'away'
    elif location == 'away':
        opp = 'home'

    team_cols = [x for x in df_wide.columns if x.startswith(location)]
    opp_cols = [x for x in df_wide.columns if x.startswith(opp)]

    df_team = df_wide[team_cols]
    df_team.columns = [x.replace(f'{location}_', '') for x in df_team.columns]

    df_opp = df_wide[opp_cols]
    df_opp.columns = [x.replace(opp, 'opp') for x in df_opp.columns]

    common_cols = [x for x in games.columns
                if not ((x.startswith('home')) or (x.startswith('away')))]

    return pd.concat([df_wide[common_cols], df_team, df_opp], axis=1)

dft = pd.concat([
    games_to_team(games, loc) for loc in ['home', 'away']], ignore_index=True)

dft['win'] = dft['pts'] > dft['opp_pts']

dft.head()

# now we can do things like look at scoring by team/bubble
g = (sns.FacetGrid(dft, hue='bubble', col='team', col_wrap=5)
     .map(sns.kdeplot, 'pts', shade=True))
g.add_legend()

#################################
# relationships between variables
#################################

# fg pct vs pts
sns.relplot(x='fg_pct', y='pts', data=dft)
plt.show()

# fg pct vs pts - win/loss
sns.relplot(x='fg_pct', y='pts', hue='win', data=dft)
plt.show()

# fg pct vs pts - win/loss
sns.relplot(x='fg3_pct', y='pts', col='team', hue='win', col_wrap=5, data=dft)
plt.show()

#############
# correlation
#############

dft[['pts', 'reb', 'win', 'fg3_pct', 'fgm', 'blk', 'opp_fg3_pct']].corr()

# scatter plot of 0.43 correlation
g = sns.relplot(x='fg3_pct', y='fgm', data=dft)
plt.show()

# scatter plot of -0.33 correlation
g = sns.relplot(x='opp_fg3_pct', y='reb', data=dft)
plt.show()

# scatter plot of 0.83 correlation
g = sns.relplot(x='fgm', y='pts', data=dft)
plt.show()

########################
# line plots with python
########################

teams = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))

dft = pd.merge(dft, teams[['team', 'division', 'conference']])

g = sns.relplot(x='month', y='pts', kind='line', data=dft.query("~bubble"),
                hue='conference')
plt.show()

# max points by month and conference
max_pts = (dft.query("~bubble").groupby(['conference', 'month'], as_index=False)['pts'].max())

g = sns.relplot(x='month', y='pts', kind='line', data=max_pts,
                hue='conference')
plt.show()

##############
# plot options
##############

# basic plot
g = (sns.FacetGrid(df, col='shot_type', hue='made')
     .map(sns.kdeplot, 'dist', shade=True))

# wrap columns
g = (sns.FacetGrid(df, col='shot_type', hue='made', col_wrap=3)
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

#############
# shot charts
#############

map_img = mpimg.imread('/Users/nathanbraun/fantasymath/basketball/nba_court.jpg')

g = sns.relplot(data=df, x='x', y='y', kind='scatter', s=5)
g.set(xlim=(-250, 250), ylim=(-50, 400), yticks=[], xticks=[], xlabel=None,
      ylabel=None)
g.despine(left=True, bottom=True)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-250, 250, -30, 400])

g.savefig(path.join(FIG_DIR, 'basic.png'))

plt.show()

g = sns.relplot(data=df, x='x', y='y', hue='made', kind='scatter',
                col='team', col_wrap=6, aspect=1.2, height=2)
g.set(xlim=(-250, 250), ylim=(-30, 400), yticks=[], xticks=[], xlabel=None,
      ylabel=None)
g.despine(left=True, bottom=True)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-250, 250, -40, 400])
g.savefig(path.join(FIG_DIR, 'shot_chart_team_made.png'))

g = sns.relplot(data=df, x='x', y='y', hue='shot_type', kind='scatter',
                col='team', col_wrap=6, aspect=1.2, height=2)
g.set(xlim=(-250, 250), ylim=(-30, 400), yticks=[], xticks=[], xlabel=None,
      ylabel=None)
g.despine(left=True, bottom=True)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-250, 250, -50, 400])
g.savefig(path.join(FIG_DIR, 'shot_chart_team_type.png'))

# do it for some single game
map_img = mpimg.imread('/Users/nathanbraun/fantasymath/basketball/nba_court.jpg')
g = sns.relplot(data=df.query("game_id == 21900002"), x='x', y='y',
                hue='made', style='made', kind='scatter', col='name',
                col_wrap=5, aspect=1.2, height=2)
g.set(xlim=(-250, 250), ylim=(-30, 400), yticks=[], xticks=[], xlabel=None,
      ylabel=None)
g.despine(left=True, bottom=True)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-250, 250, -30, 400])

# put in a function for processing

plt.show()

g.savefig(path.join(FIG_DIR, 'shot_chart_21900002.png'))

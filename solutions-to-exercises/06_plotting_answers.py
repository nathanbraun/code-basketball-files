"""
Answers to the end of chapter exercises for Summary Stats and Visualization
chapter.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

# DATA_DIR = '/Users/nathan/fantasybook/data'
DATA_DIR = './data'

dftg = pd.read_csv(path.join(DATA_DIR, 'team_games.csv'))  # play by play data

###############################################################################
# 6.1a
###############################################################################

# Using the team game data, plot the distribution of three point attempts. Make
# sure to give your plot a title.

g = (sns.FacetGrid(dftg)
     .map(sns.kdeplot, 'fg3a', fill=True))
g.figure.subplots_adjust(top=0.9)
g.figure.suptitle('Distribution of 3 Pt Attempts')
g.savefig('./solutions-to-exercises/6-1a.png')

# Now modify your plot to show the distribution of three point attempts by
# whether the team won. Do it (b) as separate colors on the same plot, and (c)
# as separate plots.

# 6.1b
g = (sns.FacetGrid(dftg, hue='wl')
    .map(sns.kdeplot, 'fg3a', fill=True))
g.figure.subplots_adjust(top=0.9)
g.figure.suptitle('Distribution of 3 Pt Attempts by Win/Loss B')
g.savefig('./solutions-to-exercises/6-1b.png')

# 6.1c
g = (sns.FacetGrid(dftg, col='wl')
    .map(sns.kdeplot, 'fg3a', fill=True))
g.figure.subplots_adjust(top=0.8)
g.figure.suptitle('Distribution of 3 Pt Attempts by Win/Loss C')
g.savefig('./solutions-to-exercises/6-1c.png')

# (d) Sometimes it's effective to use the multiple keywords ("levers") to
# display redundant information, experiment with this.

g = (sns.FacetGrid(dftg, col='wl', hue='wl')
    .map(sns.kdeplot, 'fg3a', fill=True))
g.figure.subplots_adjust(top=0.8)
g.figure.suptitle('Distribution of 3 Pt Attempts by Win/Loss D')
g.savefig('./solutions-to-exercises/6-1d.png')

# (e) Plot the three point attempts by team, with each team is on it's own
# plot. Make sure to limit the number of columns so your plot isn't just one
# wide row.

g = (sns.FacetGrid(dftg, col='team', col_wrap=6)
    .map(sns.kdeplot, 'fg3a', fill=True))
g.figure.subplots_adjust(top=0.9)
g.figure.suptitle('Distribution of 3 Pt Attempts by Team')
g.savefig('./solutions-to-exercises/6-1e.png')

# #### 6.2
# (a) Plot the relationship between three point attemtps and free throw
# percentage. Again, make sure your plot has a title.

g = sns.relplot(x='fg3a', y='ft_pct', data=dftg)
g.figure.subplots_adjust(top=0.9)
g.figure.suptitle('3 Pt Attempts vs. Free Throw %')
g.savefig('./solutions-to-exercises/6-2a.png')

# (b) Jitter three point attempts and run the scatter plot again.
import random

dftg['fg3a_jitter'] = dftg['fg3a'].apply(lambda x: x + random.gauss(0, 1))
dftg['ft_pct_jitter'] = dftg['ft_pct'].apply(lambda x: x + random.gauss(0, 0.01))

g = sns.relplot(x='fg3a_jitter', y='ft_pct_jitter', data=dftg)
g.figure.subplots_adjust(top=0.9)
g.figure.suptitle('3 Pt Attempts vs. Free Throw % Jittered')
g.savefig('./solutions-to-exercises/6-2b.png')

# (c) It's hard to tell whether this cloud of points is moving upward to the
# right or not. Check the correlation between these two variables numerically.

dftg[['fg3a', 'ft_pct']].corr()


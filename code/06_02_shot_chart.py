import pandas as pd
import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from os import path

pd.options.mode.chained_assignment = None
%matplotlib qt

# directories
DATA_DIR = './data'

# load data
dfs = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))  
dfg = pd.read_csv(path.join(DATA_DIR, 'games.csv'))  
dft = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))

# process data
cats2 = ['layup', 'pullup', 'float', 'dunk', 'hook', 'fadeaway', 'step']
dfs['jump'] = dfs[cats2].sum(axis=1) == 0

dfs['shot_type'] = np.nan
for shot in cats2 + ['jump']:
    dfs.loc[dfs[shot], 'shot_type'] = shot

#############
# shot charts
#############

# Shot Charts As Seaborn Scatter Plots

dfs[['name', 'dist', 'value', 'made', 'x', 'y']].head()

# all shot data
g = sns.relplot(data=dfs, x='x', y='y', kind='scatter', s=5)
g.set(xlim=(-250, 250), ylim=(-50, 400), yticks=[], xticks=[], xlabel=None,
      ylabel=None)
g.despine(left=True, bottom=True)

# adding background
map_img = mpimg.imread(path.join(DATA_DIR, 'nba_court.jpg'))

g = sns.relplot(data=dfs, x='x', y='y', kind='scatter', s=5)
g.set(xlim=(-250, 250), ylim=(-50, 400), yticks=[], xticks=[], xlabel=None,
      ylabel=None)
g.despine(left=True, bottom=True)

for ax in g.figure.axes:
    ax.imshow(map_img, zorder=0, extent=[-250, 250, -30, 400])

# putting in a function
def shot_chart(dfs, **kwargs):
    g = sns.relplot(data=dfs, x='x', y='y', kind='scatter', **kwargs)
    g.set(xlim=(-250, 250), ylim=(-30, 400), yticks=[], xticks=[], xlabel=None,
          ylabel=None)
    g.despine(left=True, bottom=True)

    for ax in g.figure.axes:
        ax.imshow(map_img, zorder=0, extent=[-250, 250, -30, 400])

    return g

### kwargs

def add2(num1, num2):  
    return num1 + num2

# commented out - throws an error
# add2(num1=4, num2=5, num3=1)  

def add2_flexible(num1, num2, **kwargs):
    return num1 + num2

add2_flexible(num1=4, num2=5, num3=1, num4=4)

# hue, s in **kwargs
g = shot_chart(dfs, hue='made', style='made', s=15)

g = shot_chart(dfs, hue='made', col='team', col_wrap=6, aspect=1.2, height=2)

# do it for some single game
g = shot_chart(dfs.query("game_id == 21900002"), hue='made', style='made',
        col='name', col_wrap=5, aspect=1.2, height=2)

### Contour Plots
g = (sns.FacetGrid(dfs, col='shot_type', col_wrap=3)
     .map(sns.kdeplot, 'x', 'y', alpha=0.5, fill=True)
     .add_legend())
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
for ax in g.figure.axes:
    ax.imshow(map_img, zorder=0, extent=[-250, 250, -30, 400])

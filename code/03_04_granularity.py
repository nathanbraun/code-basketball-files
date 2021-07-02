import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

BB = '/Users/nathanbraun/fantasymath/basketball/nba_api/data'
SO = '/Users/nathanbraun/fantasymath/soccer/worldcup/data'
HY = '/Users/nathanbraun/fantasymath/hockey/data'

shots = pd.read_csv(path.join(BB, 'shots.csv'))  # shot data

# Granularity

# Grouping
shots.groupby('game_id').sum()

shots['fg3m'] = (shots['value'] == 3) & shots['made']
shots['fg3a'] = (shots['value'] == 3)
shots['fga'] = 1

sum_cols = ['fgm', 'fga', 'fg3m', 'fg3a']

shots.groupby('game_id').sum()[sum_cols]

shots.groupby('game_id').agg({
    'value': 'mean',
    'dist': ['mean', 'max'],
    'fgm': 'sum',
    'fga': 'sum',
    'fg3m': 'sum',
    'fg3a': 'sum'})

shots.groupby('game_id').agg(
    ave_value = ('value', 'mean'),
    ave_dist= ('dist', 'mean'),
    max_dist  = ('dist', 'max'),
    fgm = ('fgm', 'sum'),
    fga = ('fga', 'sum'),
    fg3m = ('fg3m', 'sum'),
    fg3a = ('fg3a', 'sum'))

shots_per_pg = shots.groupby(['game_id', 'player_id']).agg(
    name = ('name', 'first'),
    fgm = ('fgm', 'sum'),
    fga = ('fga', 'sum'),
    fg3m = ('fg3m', 'sum'),
    fg3a = ('fg3a', 'sum'),
    ave_dist= ('dist', 'mean'),
    max_dist  = ('dist', 'max'),
)
shots_per_pg.head()

# A note on multilevel indexing
shots_per_pg.loc[[(21900002, 2544), (21900008, 201143)]]

# Stacking and unstacking data
sv = (shots
      .groupby(['team', 'value'])['made']
      .sum()
      .reset_index())

sv.head()

sv_reshaped = sv.set_index(['team', 'value']).unstack()
sv_reshaped.head()

total_made = sv_reshaped.sum(axis=1)
total_made.head()

sv_reshaped.columns = [2, 3]
sv_reshaped[3]/total_made

sv_reshaped.stack().head()


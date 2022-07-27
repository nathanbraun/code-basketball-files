import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = './data'

# load player-game data
pg = pd.read_csv(path.join(DATA_DIR, 'player_game.csv'))

# book picks up here:

# creating and modifying columns
pg['pts_per_shot'] = 2
pg[['game_id', 'player_id', 'pts_per_shot']].head()

pg['pts_per_shot'] = 3
pg[['game_id', 'player_id', 'pts_per_shot']].head()

# math and number columns
pg['pts_from_fgs'] = (pg['fg3m']*3 + (pg['fgm'] - pg['fg3m'])*2)
pg[['name', 'game_id', 'pts_from_fgs']].head()

import numpy as np  # note: normally you'd import this at the top of the file

pg['biggest_impact'] = np.abs(pg['plus_minus'])

pg['ln_pts'] = np.log(pg['pts'])

pg['court_length'] = 94

pg[['name', 'game_id', 'court_length']].sample(5)

# string columns
pg['name'].str.upper().sample(5)

pg['name'].str.replace('.', ' ').sample(5)

(pg['name'] + ', ' + pg['team']).sample(5)

pg['name'].str.replace('.', ' ').str.lower().sample(5)

# boolean columns
pg['is_a_guard'] = (pg['pos'] == 'Guard')
pg[['name', 'is_a_guard']].sample(5)

pg['is_a_forward_or_center'] = (pg['pos'] == 'Forward') | (pg['pos'] == 'Center')
pg['good_guard_game'] = (pg['pos'] == 'Guard') & (pg['pts'] >= 30)
pg['not_gt_10_pts_or_assists'] = ~((pg['pts'] > 10) | (pg['ast'] > 10))

(pg[['pts', 'ast']] > 10).sample(5)

# Applying functions to columns
def is_w_pac(team):
  """
  Takes some string named team ('MIL', 'LAL', 'CHI' etc) and checks
  whether it's in the Pacific Division.
  """
  return team in ['LAC', 'LAL', 'PHX', 'SAC', 'GSW']

pg['is_w_pac'] = pg['team'].apply(is_w_pac)

pg[['name', 'team', 'is_w_pac']].sample(5)

pg['is_w_pac_alternate'] = pg['team'].apply(
    lambda x: x in ['LAC', 'LAL', 'PHX', 'SAC', 'GSW'])

# Dropping Columns
pg.drop('is_w_pac_alternate', axis=1, inplace=True)

# Renaming Columns
pg.columns = [x.upper() for x in pg.columns]

pg.head()

pg.columns = [x.lower() for x in pg.columns]

pg.rename(columns={'fgm': 'field_goals_made'}, inplace=True)

# missing data
pg['ft_pct'] = pg['ftm']/pg['fta']
pg[['name', 'team', 'ftm', 'fta', 'ft_pct']].head()

pg['ft_pct'].isnull().head()

pg['ft_pct'].notnull().head()

pg['ft_pct'].fillna(-99).head()

# Changing column types
pg['date'].sample(5)

date = '20191119'

year = date[0:4]
month = date[4:6]
day = date[6:8]

year
month
day

# pg['month'] = pg['date'].str[4:6]  # commented out since it gives an error

pg['month'] = pg['date'].astype(str).str[4:6]
pg[['name', 'team', 'month', 'date']].sample(5)

pg['month'].astype(int).sample(5)

pg.dtypes.head()

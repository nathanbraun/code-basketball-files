import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

BB = '/Users/nathanbraun/fantasymath/basketball/nba_api/data'
SO = '/Users/nathanbraun/fantasymath/soccer/worldcup/data'
HY = '/Users/nathanbraun/fantasymath/hockey/data'

# load player-game data
pg = pd.read_csv(path.join(BB, 'player_game.csv'))

pg[['game_id', 'player_id', 'date']] = (
    pg[['game_id', 'player_id', 'date']].astype(str))

# book picks up here:
pg.mean()
pg.max()

# Axis
pg[['pts', 'ast', 'stl', 'reb']].mean(axis=0)
pg[['pts', 'ast', 'stl', 'reb']].mean(axis=1).head()

# Summary functions on boolean columns
pg['cold_shooting'] = (pg['fga'] > 10) & (pg['pts'] < 5)
pg['cold_shooting'].mean()

pg['cold_shooting'].sum()

(pg['fg3a'] > 30).any()
(pg['fg3a'] > 20).any()

(pg['min'] > 0).all()

pg['center_w_five_3s'] = (pg['pos'] == 'Center') & (pg['fg3m'] >= 5)

pg['center_w_five_3s'].mean()
pg['center_w_five_3s'].sum()

(pg[['pts', 'ast', 'reb', 'stl', 'blk']] > 10).any(axis=1)

pg['triple_double'] = ((pg[['pts', 'ast', 'reb', 'stl', 'blk']] > 10)
                       .sum(axis=1) == 3)

# Other misc built-in summary functions
pg['pos'].value_counts()

pg['pos'].value_counts(normalize=True)

pd.crosstab(pg['team'], pg['pos']).head()

import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'
 
DATA_DIR = './data'

pg = pd.read_csv(path.join(DATA_DIR, 'player_game.csv'))  # player-game
games = pd.read_csv(path.join(DATA_DIR, 'games.csv'))  # game info
player = pd.read_csv(path.join(DATA_DIR, 'players.csv')) # player info

pg['fg2m'] = pg['fgm'] - pg['fg3m']
pg['fg2a'] = pg['fga'] - pg['fg3a']

# player game data
pg[['name', 'team', 'game_id', 'fga', 'ast', 'stl', 'pts']].head(5)

# game table
games[['game_id', 'date', 'home', 'away']].head()

# chapter picks up here:
# Merge Question 1. What columns are you joining on?
pd.merge(pg, games[['game_id', 'home', 'away']], on='game_id').head()

pg['fg2m'] = pg['fgm'] - pg['fg3m']
pg['fg2a'] = pg['fga'] - pg['fg3a']

df2 = pg[['game_id', 'player_id', 'fg2m', 'fg2a']]
df3 = pg[['game_id', 'player_id', 'fg3m', 'fg3a']]

combined = pd.merge(df2, df3, on=['player_id', 'game_id'])

# Merge Question 2. Are you doing a 1:1, 1:many (or many:1), or many:many
# join?player.head()

combined.head()

player[['player_id', 'name', 'team', 'height', 'weight']].head()

player['player_id'].duplicated().any()

combined['player_id'].duplicated().any()

pd.merge(combined, player[['player_id', 'name', 'height', 'weight']]).head()

# pd.merge(combined, player, validate='1:1')  # this will fail since it's 1:m

# Merge Question 3. What are you doing with unmatched observations?
df2 = pg.loc[pg['fg2a'] > 0, ['game_id', 'player_id', 'fg2m', 'fg2a']]

df3 = pg.loc[pg['fg3a'] > 0, ['game_id', 'player_id', 'fg3m', 'fg3a']]

df2.shape
df3.shape

comb_inner = pd.merge(df2, df3)
comb_inner.shape

comb_left = pd.merge(df2, df3, how='left')
comb_left.shape

comb_left.head()

comb_outer = pd.merge(df2, df3, how='outer', indicator=True)
comb_outer.shape

comb_outer['_merge'].value_counts()

# More on pd.merge
# left_on and right_on
df2.columns = ['game_id', 'fg2_shooter_id', 'fg2m', 'fg2a']

df3.columns = ['game_id', 'fg3_shooter_id', 'fg3m', 'fg3a']

pd.merge(df2, df3, left_on=['game_id', 'fg2_shooter_id'],
    right_on=['game_id', 'fg3_shooter_id']).head()

# merging on index
max_fg3 = (df3
           .groupby('fg3_shooter_id')
           .agg(max_fg3m = ('fg3m', 'max'),
                max_fg3a =  ('fg3a', 'max')))

max_fg3.head()

pd.merge(df3, max_fg3, left_on='fg3_shooter_id', right_index=True).sample(5)

#############
# pd.concat()
#############
df2 = (pg.loc[pg['fg2a'] > 0, ['game_id', 'player_id', 'fg2m', 'fg2a']]
       .set_index(['game_id', 'player_id']))

df3 = (pg.loc[pg['fg3a'] > 0, ['game_id', 'player_id', 'fg3m', 'fg3a']]
       .set_index(['game_id', 'player_id']))

df2.head()

pd.concat([df2, df3], axis=1).head()

df_ft = (pg.loc[pg['fta'] > 0, ['game_id', 'player_id', 'ftm', 'fta']]
           .set_index(['game_id', 'player_id']))

pd.concat([df2, df3, df_ft], axis=1).head()

#### Combining DataFrames Vertically
bucks = pg.loc[pg['team'] == 'MIL']
magic = pg.loc[pg['team'] == 'ORL']

bucks.shape
magic.shape

pd.concat([bucks, magic]).shape

bucks_reset = bucks.reset_index(drop=True)
magic_reset = magic.reset_index(drop=True)

bucks_reset.head()

pd.concat([bucks_reset, magic_reset]).sort_index().head()

pd.concat([bucks_reset, magic_reset], ignore_index=True).sort_index().head()

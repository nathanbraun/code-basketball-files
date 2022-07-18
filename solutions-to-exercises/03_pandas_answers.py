"""
Answers to the end of chapter exercises for Pandas chapter.

Questions with written (not code) answers are inside triple quotes.
"""
###############################################################################
# PANDAS BASICS
###############################################################################

#######
# 3.0.1
#######
import pandas as pd
from os import path

DATA_DIR = './data'
games = pd.read_csv(path.join(DATA_DIR, 'games.csv'))

#######
# 3.0.2
#######
# works because data is sorted by adp already
games50 = games.head(50)

# this is better if don't want to assume data is sorted
games50 = games.sort_values('date').head(50)

#######
# 3.0.3
#######
games.sort_values('home_pts', ascending=False, inplace=True)
games.head()

# Note: if this didn't work when you printed it on a new line in the REPL you
# probably forgot the `inplace=True` argument.

#######
# 3.0.4
#######
type(games.sort_values('home_pts'))  # it's a DataFfame

#######
# 3.0.5
#######
# a
game_simple = games[['date', 'home', 'away', 'home_pts', 'away_pts']]

# b
game_simple = game_simple[['home', 'away', 'date', 'home_pts', 'away_pts']]

# c
game_simple['game_id'] = games['game_id']

# d
games.to_csv(path.join(DATA_DIR, 'game_simple.txt'), sep='|')

###############################################################################
# COLUMNS
###############################################################################

#######
# 3.1.1
#######
import pandas as pd
from os import path

DATA_DIR = './data'
pg = pd.read_csv(path.join(DATA_DIR, 'player_game.csv'))

#######
# 3.1.2
#######
pg['net_takeaways'] = pg['stl'] - pg['tov']
pg['net_takeaways'].head()

#######
# 3.1.3
#######
pg['player_desc'] = pg['name'] + ' is the ' + pg['team'] + ' ' + pg['pos']
pg['player_desc'].head()

#######
# 3.1.4
#######
pg['bad_game'] = (pg['fga'] > 20) & (pg['pts'] < 15)
pg['bad_game'].head()

#######
# 3.1.5
#######
pg['len_last_name'] = (pg['name']
                       .apply(lambda x: len(x.split('.')[-1])))
pg['len_last_name'].head()

#######
# 3.1.6
#######
pg['game_id'] = pg['game_id'].astype(str)

#######
# 3.1.7
#######
# a
pg.columns = [x.replace('_', ' ') for x in pg.columns]
pg.head()

# b
pg.columns = [x.replace(' ', '_') for x in pg.columns]
pg.head()

#######
# 3.1.8
#######
# a
pg['oreb_percentage'] = pg['oreb']/pg['reb']
pg['oreb_percentage'].head()

# b
"""
`'oreb_percentage'` is offensive rebounds divided by total rebounds. Since you
can't divide by 0, `oreb_percentage` is missing whenever a player had 0 rebounds.
"""

# To replace all the missing values with `-99`:
pg['oreb_percentage'].fillna(-99, inplace=True)
pg['oreb_percentage'].head()

#######
# 3.1.9
#######
pg.drop('oreb_percentage', axis=1, inplace=True)
pg.head()

# If you forget the `axis=1` Pandas will try to drop the *row* with the
# index value `'oreb_percentage'`. Since that doesn't exist, it'll throw an
# error.

# Without the `inplace=True`, Pandas just returns a new copy of `pg` without the
# `'oreb_percentage'` column. Nothing happens to the original `pg`, though we
# could reassign it if we wanted like this:

# alternative to inplace=True
# pg = pg.drop('oreb_percentage', axis=1)

###############################################################################
# BUILT-IN FUNCTIONS
###############################################################################
#######
# 3.2.1
#######
import pandas as pd
from os import path

DATA_DIR = './data'
pg = pd.read_csv(path.join(DATA_DIR, 'player_game.csv'))

#######
# 3.2.2
#######
pg['total_shots1'] = pg['fga'] + pg['fta']

pg['total_shots2'] = pg[['fga', 'fta']].sum(axis=1)

(pg['total_shots1'] == pg['total_shots2']).all()

#######
# 3.2.3
#######

# a
pg[['pts', 'fga', 'reb']].mean()

# pts    10.659413
# fga     8.403500
# reb     4.242668

# b
((pg['pts'] >= 40) & (pg['reb'] >= 10)).sum()  # 3

# c
(((pg['pts'] >= 40) & (pg['reb'] >= 10)).sum()
/(pg['pts'] >= 40).sum())

# d
pg['fg3a'].sum()  # 6809

# e
pg['team'].value_counts()  # ORL - 152 times

###############################################################################
# FILTERING
###############################################################################
#######
# 3.3.1
#######
import pandas as pd
from os import path

DATA_DIR = './data'
dftg = pd.read_csv(path.join(DATA_DIR, 'team_games.csv'))

#######
# 3.3.2
#######
# a
dftg_chi1 = dftg.loc[dftg['team'] == 'CHI', ['team', 'date', 'pts', 'fgm', 'fga']]
dftg_chi1.head()

# b
dftg_chi2 = dftg.query("team == 'CHI'")[['team', 'date', 'pts', 'fgm', 'fga']]
dftg_chi2.head()

#######
# 3.3.3
#######
dftg_no_chi = dftg.loc[dftg['team'] != 'CHI', ['team', 'date', 'pts', 'fgm', 'fga']]
dftg_no_chi.head()

#######
# 3.3.4
#######

# a
dftg[['fga', 'fgm', 'fg3a', 'fg3m']].duplicated().any()  # yes there are

dftg[['fga', 'fgm', 'fg3a', 'fg3m']].duplicated().sum()  # 32

# b
# flags ALL dups (not just 2nd) because passing keep=False
dups = dftg[['fga', 'fgm', 'fg3a', 'fg3m']].duplicated(keep=False)

dftg_fg_dup = dftg.loc[dups]
dftg_fg_no_dup = dftg.loc[~dups]

#######
# 3.3.5
#######
import numpy as np

dftg['three_pt_desc'] = np.nan
dftg.loc[dftg['fg3_pct'] > .5, 'three_pt_desc'] = 'great'
dftg.loc[dftg['fg3_pct'] <= .25, 'three_pt_desc'] = 'brutal'
dftg[['fg3_pct', 'three_pt_desc']].sample(5)

#######
# 3.3.6
#######
# a
dftg_no_desc1 = dftg.loc[dftg['three_pt_desc'].isnull()]

# b
dftg_no_desc2 = dftg.query("three_pt_desc.isnull()")

###############################################################################
# GRANULARITY
###############################################################################
#######
# 3.4.1
#######
"""
Usually you can only shift your data from more (play by play) to less (game)
granular, which necessarily results in a loss of information. If I go from
knowing whether or not Lebron made every single shot to just knowing how many
points he scored totak, that's a loss of information.
"""

#######
# 3.4.2
#######

# a
import pandas as pd
from os import path

DATA_DIR = '/Users/nathan/fantasybook/data'
dftg = pd.read_csv(path.join(DATA_DIR, 'play_data_sample.csv'))

# b
(dftg
.groupby('team')['pts'].mean())

# c
dftg['gt_100'] = dftg['pts'] >= 100

(dftg
.groupby('team')['gt_100'].mean())

# d
dftg['gt_150'] = dftg['pts'] >= 150
(dftg
.groupby('team')['gt_150'].any())

# e

dftg.groupby('date')['team_id'].count().head()
dftg.groupby('date')['team_id'].sum().head()

"""
Count counts the number of non missing (non `np.nan`) values. This is different
than `sum` which adds up the values in all of the columns. The only time
`count` and `sum` would return the same thing is if you had a column filled
with 1s without any missing values.
"""

#######
# 3.4.3
#######

# a
dftg2 = dftg.groupby(['team_id', 'wl']).agg(
    ave_pts = ('pts', 'mean'),
    ave_fgm = ('fgm', 'mean'),
    ave_fga = ('fga', 'mean'),
    ave_fg3m = ('fg3m', 'mean'),
    ave_fg3a = ('fg3a', 'mean'),
    n = ('team_id', 'count'))

dftg2.head()

# b
dftg2.reset_index(inplace=True)

# c
# loc
(dftg2.loc[dftg2['wl'] == 'L', 'ave_pts'] > 110).sum()  # 4

# or with query
(dftg2.query("wl == 'L'")['ave_pts'] > 110).sum()  # 4

# d
dftg3 = dftg.groupby(['team', 'wl']).agg(
    ave_pts = ('pts', 'mean'),
    ave_fgm = ('fgm', 'mean'),
    ave_fga = ('fga', 'mean'),
    ave_fg3m = ('fg3m', 'mean'),
    ave_fg3a = ('fg3a', 'mean'),
    n = ('team', 'count'))

# e
"""
Stacking is when you change the granularity in your data, but shift information
from rows to columns (or vis versa) so it doesn't result in any loss on
information.

An example would be going from the team-win/loss level to the team level. If we
stacked it, we'd go from rows being:

            ave_pts    ave_fgm    ave_fga   ave_fg3m   ave_fg3a   n
team wl
ATL  L   107.382979  39.127660  90.936170  11.382979  36.425532  47
     W   122.050000  44.200000  89.650000  13.500000  35.200000  20
BKN  L   107.216216  39.027027  91.135135  12.459459  38.918919  37
     W   116.600000  41.828571  89.314286  13.714286  37.314286  35
BOS  L   105.416667  38.041667  90.208333  10.958333  35.541667  24

To:

     ave_pts        ave_fgm   ... ave_fg3m ave_fg3a         n
wl         L      W       L   ...        W        L     W   L   W
team                          ...
ATL    107.0  122.0    39.0   ...     14.0     36.0  35.0  47  20
BKN    107.0  117.0    39.0   ...     14.0     39.0  37.0  37  35
BOS    105.0  118.0    38.0   ...     13.0     36.0  34.0  24  48
CHA    100.0  107.0    37.0   ...     13.0     34.0  34.0  42  23
CHI    103.0  114.0    39.0   ...     14.0     36.0  34.0  43  22
"""

###############################################################################
# COMBINING DATAFRAMES
###############################################################################
#######
# 3.5.1
#######
# a
import pandas as pd
from os import path

DATA_DIR = './data'
df_pts = pd.read_csv(path.join(DATA_DIR, 'problems/combine1', 'pts.csv'))
df_reb = pd.read_csv(path.join(DATA_DIR, 'problems/combine1', 'reb.csv'))
df_def = pd.read_csv(path.join(DATA_DIR, 'problems/combine1', 'def.csv'))

# b
df_comb1 = pd.merge(df_pts, df_reb)
df_comb1 = pd.merge(df_comb1, df_def, how='left')

df_comb1 = df_comb1.fillna(0)

# c
df_comb2 = pd.concat([df_pts.set_index(['player_id', 'game_id']),
                      df_reb.set_index(['player_id', 'game_id']),
                      df_def.set_index(['player_id', 'game_id'])], join='outer',
                     axis=1)
df_comb2 = df_comb2.fillna(0)

# d
"""
Which is better is somewhat subjective, but I generally prefer `concat` when
combining three or more DataFrames because you can do it all in one step.

Note `merge` gives a little more fine grained control over how you merge (left,
or outer) vs `concat`, which just gives you inner vs outer.

Note also we have to set the index equal to game and player id before
concating.
"""

########
# 3.5.2a
########
import pandas as pd
from os import path

DATA_DIR = './data'
df_c = pd.read_csv(path.join(DATA_DIR, 'problems/combine2', 'center.csv'))
df_f = pd.read_csv(path.join(DATA_DIR, 'problems/combine2', 'forward.csv'))
df_g = pd.read_csv(path.join(DATA_DIR, 'problems/combine2', 'guard.csv'))

# b
df = pd.concat([df_c, df_f, df_g], ignore_index=True)

#######
# 3.5.3
#######
# a
import pandas as pd
from os import path

DATA_DIR = './data'
dft = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))

# b
for conf in ['East', 'West']:
    (dft
        .query(f"conference == '{conf}'")
        .to_csv(path.join(DATA_DIR, f'dft_{conf}.csv'), index=False))

# c
df = pd.concat([pd.read_csv(path.join(DATA_DIR, f'dft_{conf}.csv'))
    for conf in ['East', 'West']], ignore_index=True)


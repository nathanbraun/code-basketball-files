import pandas as pd
import numpy as np
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = './data'

# note: we're passing the index_col argument, which immediately setting the
# index to be the player_id column

dfp = pd.read_csv(path.join(DATA_DIR, 'players.csv'), index_col='player_id')

# Filtering
lebron_id = 2544
dfp.loc[lebron_id]

laker_ids = ([2544, 203076, 201566])

dfp.loc[laker_ids]
dfp.loc[laker_ids, ['name', 'school', 'height', 'weight']]
dfp.loc[laker_ids, 'name']

# Boolean Indexing
school_in_nc = dfp['school'] == 'North Carolina'

school_in_nc.head()

players_nc = dfp.loc[school_in_nc]

players_nc[['name', 'school', 'height', 'weight']].head()
players_duke = dfp.loc[dfp['school'] == 'Duke']

players_duke[['name', 'school', 'height', 'weight']].head()

from_usa = dfp['country'] == 'USA'

players_not_usa = dfp.loc[~from_usa]

players_not_usa[['name', 'country', 'height', 'weight']].head()

# Duplicates
dfp.drop_duplicates(inplace=True)

dfp.drop_duplicates('pos')[['name', 'pos', 'height', 'weight']]

dfp.duplicated().head()

dfp['pos'].duplicated().head()

dfp.drop_duplicates('pos')
dfp.loc[~dfp['pos'].duplicated()]

# Combining filtering with changing columns
dfp['draft_desc'] = ''
dfp.loc[dfp['draft_round'] == 1, 'draft_desc'] = 'first round'
dfp.loc[(dfp['draft_round'] == 1) & (dfp['draft_number'] <= 14), 'draft_desc'] = 'lottery'
dfp.loc[(dfp['draft_round'] == 1) & (dfp['draft_number'] <= 5), 'draft_desc'] = 'top 5'
dfp.loc[dfp['draft_round'] == 2, 'draft_desc'] = 'second round'
dfp.loc[dfp['draft_round'].isnull(), 'draft_desc'] = 'undrafted'

dfp[['name', 'school', 'draft_round', 'draft_number', 'draft_desc']].sample(5)

# Query
dfp.query("school == 'North Carolina'").head()

dfp['school_in_kentucky'] = dfp['school'] == 'Kentucky'

dfp.query("school_in_kentucky").head()

dfp.query("draft_round.isnull()")[['name', 'school', 'draft_round', 'draft_number']].head()

# note: if getting an error on line above, try it with engine='python' like
# this
dfp.query("draft_round.isnull()", engine='python')[['name', 'school', 'draft_round', 'draft_number']].head()

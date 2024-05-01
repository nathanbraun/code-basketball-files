import requests
import json
from pandas import DataFrame
import pandas as pd

BDL_API_KEY = 'PUT_YOUR_API_KEY_HERE'

# players
players_url = 'https://api.balldontlie.io/v1/players'

AUTH_HEADER = {'Authorization': BDL_API_KEY}

players_resp = requests.get(players_url, headers=AUTH_HEADER)
players_json = players_resp.json()

# with open('./data/json/players.json') as f:
#     players_json = json.load(f)

players_json
players_json.keys()

type(players_json)

type(players_json['data'])
player0 = players_json['data'][0]
player0

player0_flat = {key: value for key, value in player0.items() if type(value) not
    in (dict, list)}

player0_flat
player0['team']
player0_flat['team_id'] = player0['team']['id']
player0_flat['team'] = player0['team']['abbreviation']
player0_flat['conference'] = player0['team']['conference']

player0_flat

def flatten_player(nested):
    flat = {key: value for key, value in nested.items() if type(value) not in
        (dict, list)}
    flat['team_id'] = nested['team']['id']
    flat['team'] = nested['team']['abbreviation']
    flat['conference'] = nested['team']['conference']

    return flat


df_players = DataFrame([flatten_player(x) for x in players_json['data']])
df_players.head()

# pagination
players_json['meta']

players25 = (requests
  .get('https://api.balldontlie.io/v1/players/?cursor=25', headers=AUTH_HEADER)
  .json())

players25['meta']

players50_100 = (requests
  .get('https://api.balldontlie.io/v1/players/?cursor=25&per_page=100', headers=AUTH_HEADER)
  .json())

len(players50_100['data'])

def get_players_cursor(cursor):
    players_json = (requests
        .get(f'https://api.balldontlie.io/v1/players/?cursor={cursor}',
             headers=AUTH_HEADER)
        .json())
    
    return DataFrame([flatten_player(x) for x in players_json['data']])

df25 = get_players_cursor(25)
df25.head()

# return next cursor too

def get_players_cursor_wnext(cursor):
    players_json = (requests
        .get(f'https://api.balldontlie.io/v1/players/?cursor={cursor}',
             headers=AUTH_HEADER)
        .json())
    
    return (
        DataFrame([flatten_player(x) for x in players_json['data']]),
        players_json['meta']['next_cursor'])

df25, next = get_players_cursor_wnext(25)
df25.head()

players_json = (requests
    .get('https://api.balldontlie.io/v1/players/?cursor=100000000',
         headers=AUTH_HEADER)
    .json())
players_json

if 'next_cursor' in players_json['meta']:
    next = players_json['meta']['next_cursor']
else:
    next = None

next = players_json['meta'].get('next_cursor')
next

def get_players_cursor_wnext2(cursor):
    players_json = (requests
        .get(f'https://api.balldontlie.io/v1/players/?cursor={cursor}',
             headers=AUTH_HEADER)
        .json())
    
    return (
        DataFrame([flatten_player(x) for x in players_json['data']]),
        players_json['meta'].get('next_cursor'))


i = 0
while i < 5:
    print(i)
    i = i + 1

df_all_players = DataFrame()

cursor = 200  # start here - just showing how it works
df_working, next_cursor = get_players_cursor_wnext2(cursor)

while (next_cursor is not None) and (next_cursor <= 500):
    # add the current df_working_page to the dataframe of all the players
    df_all_players = pd.concat([df_all_players, df_working],
                               ignore_index=True)

    # get the next page of data
    print(f'getting cursor {next_cursor}')
    df_working, next_cursor = get_players_cursor_wnext2(next_cursor)

df_all_players.sample(10)
df_all_players.shape


################################################################################
################################################################################

## note: this part isn't meant to be run
## i (nate) am running this Wed 5/1/24 to save data we'll load above
## 
## including here to make it clearer this saved data above just comes from APIs

# players_url = 'https://api.balldontlie.io/v1/players'

# players_resp = requests.get(players_url, headers=AUTH_HEADER)

# players_json = players_resp.json()

# with open('./data/json/players.json', 'w') as f:
#     json.dump(players_json, f)

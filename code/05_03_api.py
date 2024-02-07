import requests
import json
from pandas import DataFrame
import pandas as pd

# players
players_url = 'https://www.balldontlie.io/api/v1/players'
players_resp = requests.get(players_url)
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
player0_flat['team_id'] = player0['team']['id']
player0_flat['team'] = player0['team']['abbreviation']
player0_flat['conference'] = player0['team']['conference']

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

players1 = (requests
    .get('https://www.balldontlie.io/api/v1/players?page=1')
    .json())

players1['meta']

players2 = (requests
    .get('https://www.balldontlie.io/api/v1/players?page=2')
    .json())

players2['meta']

players2_100 = (requests
    .get('https://www.balldontlie.io/api/v1/players?page=2&per_page=100')
    .json())

len(players2_100['data'])

def get_players_page(page):
    players_json = (requests
        .get(f'https://www.balldontlie.io/api/v1/players?page={page}')
        .json())
    
    return DataFrame([flatten_player(x) for x in players_json['data']])

def get_players_page_wnext(page):
    players_json = (requests
        .get(f'https://www.balldontlie.io/api/v1/players?page={page}')
        .json())
    
    return (
        DataFrame([flatten_player(x) for x in players_json['data']]),
        players_json['meta']['next_page'])

df1 = get_players_page(1)
df1.head()

df2 = get_players_page(2)
df2.head()

df1M = get_players_page(1000000)
df1M

i = 0
while i < 5:
    print(i)
    i = i + 1

df_all_players = DataFrame()

page = 200  # start here - just showing how it works
df_working_page = get_players_page(page)

while not df_working_page.empty:
    # add the current df_working_page to the dataframe of all the players
    df_all_players = pd.concat([df_all_players, df_working_page],
                               ignore_index=True)

    # get the next page of data
    page = page + 1
    print(f'getting page {page}')
    df_working_page = get_players_page(page)

df_all_players.sample(10)
df_all_players.shape


################################################################################
################################################################################

## note: this part isn't meant to be run
## i (nate) am running this Wed 2/7/24 to save data we'll load above
## 
## including here to make it clearer this saved data above just comes from APIs

# players_url = 'https://www.balldontlie.io/api/v1/players'

# players_resp = requests.get(players_url)

# players_json = players_resp.json()

# with open('./data/json/players.json', 'w') as f:
#     json.dump(players_json, f)

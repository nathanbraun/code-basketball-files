import requests
import json
from pandas import DataFrame
import pandas as pd

teams_url = 'http://data.nba.net/prod/v1/2021/teams.json'
teams_resp = requests.get(teams_url)
teams_json = teams_resp.json()

# with open('./data/json/teams.json') as f:
#     teams_json = json.load(f)

teams_json
teams_json.keys()

type(teams_json)

type(teams_json['league']['standard'])

teams_json['league']['standard'][0]

df_teams = DataFrame(teams_json['league']['standard'])
df_teams.head()

# roster
players_url = 'http://data.nba.net/prod/v1/2021/players.json'
players_resp = requests.get(players_url)
players_json = players_resp.json()

# with open('./data/json/players.json') as f:
#     players_json = json.load(f)

player0 = players_json['league']['standard'][0]

player_cols = [key for key, value in player0.items() if type(value) is not
        (dict or list)]

df_players = DataFrame(players_json['league']['standard'])[player_cols]
df_players.head()

player0['teams']

DataFrame(player0['teams'])

def player_teams_to_df(player_dict):
    df = DataFrame(player_dict['teams'])
    df['personId'] = player_dict['personId']
    return df

player_teams_to_df(player0)

df_player_team = pd.concat([player_teams_to_df(x) for x in
    players_json['league']['standard']], ignore_index=True)

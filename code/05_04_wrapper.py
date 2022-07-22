from pandas import DataFrame, Series
import pandas as pd

# book starts here
# starting with team annd player ids
from nba_api.stats.static import teams, players

player_df = DataFrame(players.get_players())
player_df.head()

team_df = DataFrame(teams.get_teams())
team_df.head()

from nba_api.stats.endpoints.commonplayerinfo import CommonPlayerInfo

from nba_api.stats.endpoints.teamyearbyyearstats import TeamYearByYearStats

teams_df.head()

pelicans_id = '1610612740'
pelicans_data = TeamYearByYearStats(pelicans_id)
pelicans_data

pelicans_df = pelicans_data.get_data_frames()[0]
pelicans_df.head()

# play by play example
from nba_api.stats.endpoints.playbyplayv2 import PlayByPlayV2
PlayByPlayV2?


game_id = '0021700807'
pbp_data = PlayByPlayV2(game_id)
pbp_data

pbp_df = pbp_data.get_data_frames()[0]

from nba_api.stats.endpoints.teamgamelog import TeamGameLog
TeamGameLog?

team_df.query("abbreviation == 'MIL'")[['id', 'full_name']]
bucks_id = '1610612749'

mil_log = TeamGameLog(bucks_id).get_data_frames()[0]

mil_game_ids = list(mil_log['Game_ID'].head())
mil_game_ids

mil_pbp_df1 = pd.concat([
    PlayByPlayV2(x).get_data_frames()[0] for x in mil_game_ids],
    ignore_index=True)

mil_pbp_df1.head()

# commented out since it throws an error
# PlayByPlayV2('XXXXXXXXXX')  

def get_pbp_data(game_id):
    try:
        pbp_df = PlayByPlayV2(game_id).get_data_frames()[0]
    except Exception as _:
        pbp_df = DataFrame()

    return pbp_df

get_pbp_data('0021700807')
get_pbp_data('XXXXXXXXXX')

mil_game_ids = mil_game_ids + ['XXXXXXXXXX']
mil_game_ids

pbp_df_all = DataFrame()
bad_game_ids = []
for gid in mil_game_ids:
    print(gid)
    try:
        working_df = PlayByPlayV2(gid).get_data_frames()[0]
    except Exception as _:
        bad_game_ids = bad_game_ids + [gid]
        continue  # continue means stop here and go to next item in the for loop

    pbp_df_all = pd.concat([pbp_df_all, working_df], ignore_index=True)

pbp_df_all['GAME_ID'].value_counts()
bad_game_ids


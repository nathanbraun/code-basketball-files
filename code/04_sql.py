import pandas as pd
from os import path
import sqlite3

###############################################
# loading csvs and putting them in a sqlite db
###############################################

# only need to run this section once

# handle directories
BB = '/Users/nathanbraun/fantasymath/basketball/nba_api/data'
SO = '/Users/nathanbraun/fantasymath/soccer/worldcup/data'
HY = '/Users/nathanbraun/fantasymath/hockey/data'

# create connection
conn = sqlite3.connect(path.join(BB, 'ltcwbb.sqlite'))

# load csv data
player_game = pd.read_csv(path.join(BB, 'player_game.csv'))
player = pd.read_csv(path.join(BB, 'players.csv'))

game = pd.read_csv(path.join(BB, 'games.csv'))
team = pd.read_csv(path.join(BB, 'teams.csv'))

# and write it to sql
player_game.to_sql('player_game', conn, index=False, if_exists='replace')
player.to_sql('player', conn, index=False, if_exists='replace')

game.to_sql('game', conn, index=False, if_exists='replace')
team.to_sql('team', conn, index=False, if_exists='replace')

#########
# Queries
#########
conn = sqlite3.connect(path.join(BB, 'ltcwbb.sqlite'))

# return entire player table
df = pd.read_sql(
    """
    SELECT *
    FROM player
    """, conn)
df.head()

# return specific columns from player table + rename on the fly
df = pd.read_sql(
    """
    SELECT player_id, name, birthdate as bday
    FROM player
    """, conn)
df.head()

###########
# filtering
###########

# basic filter, only rows where team is MIA
df = pd.read_sql(
    """
    SELECT player_id, name, birthdate as bday
    FROM player
    WHERE country = 'Canada'
    """, conn)
df.head()

# AND in filter
df = pd.read_sql(
    """
    SELECT player_id, name, pos, country
    FROM player
    WHERE country != 'USA' AND pos == 'Center'
    """, conn)
df.head()

# OR in filter
df = pd.read_sql(
    """
    SELECT player_id, name, pos, country, school
    FROM player
    WHERE country != 'USA' OR school = 'North Carolina'
    """, conn)
df.head()

# IN in filter
df = pd.read_sql(
    """
    SELECT player_id, name, pos, country, school
    FROM player
    WHERE school IN ('North Carolina', 'Duke')
    """, conn)

# negation with NOT
df = pd.read_sql(
    """
    SELECT player_id, name, pos, country, school
    FROM player
    WHERE school NOT IN ('North Carolina', 'Duke')
    """, conn)

#########
# joining
#########

# no WHERE so fullcrossjoin
df = pd.read_sql(
    """
    SELECT
        player.name,
        player.pos,
        player.team,
        team.conference,
        team.division
    FROM player, team
    """, conn)
df.head(10)

# add in two team columns to make clearer
df = pd.read_sql(
    """
    SELECT
        player.name,
        player.pos,
        player.team as player_team,
        team.team as team_team,
        team.conference,
        team.division
    FROM player, team
    """, conn)
df.head(10)

# n of rows
df.shape

# works when we add WHERE to filter after crossjoin
df = pd.read_sql(
    """
    SELECT
        player.name,
        player.pos,
        player.team,
        team.conference,
        team.division
    FROM player, team
    WHERE player.team = team.team
    """, conn)
df.head()

# add in team column to make clearer how it works
df = pd.read_sql(
    """
    SELECT
        player.name,
        player.pos,
        player.team as player_team,
        team.team as team_team,
        team.conference,
        team.division
    FROM player, team
    WHERE player.team = team.team
    """, conn)
df.head()

# adding a third table
df = pd.read_sql(
    """
    SELECT
        player.name,
        player.pos,
        team.team,
        team.conference,
        team.division,
        player_game.*
    FROM player, team, player_game
    WHERE
        player.team = team.team AND
        player_game.player_id = player.player_id
    """, conn)
df.head()

# adding a third table - shorthand
df = pd.read_sql(
    """
    SELECT
        p.name,
        p.pos,
        t.team,
        t.conference,
        t.division,
        pg.*
    FROM player AS p, team AS t, player_game AS pg
    WHERE
        p.team = t.team AND
        pg.player_id = p.player_id
    """, conn)
df.head()

# adding an additional filter
df = pd.read_sql(
    """
    SELECT
        p.name,
        p.pos,
        t.team,
        t.conference,
        t.division,
        pg.*
    FROM player AS p, team AS t, player_game AS pg
    WHERE
        p.team = t.team AND
        pg.player_id = p.player_id AND
        p.pos == 'Center'
    """, conn)
df.head()

###########
# LIMIT/TOP
###########

# SELECT *
# FROM player
# LIMIT 5

# SELECT TOP 5 *
# FROM player

df = pd.read_sql(
    """
    SELECT DISTINCT season, date
    FROM game
    """, conn)
df.head()

# UNION
# SUBQUERIES
# LEFT, RIGHT, OUTER JOINS

# SELECT *
# FROM <left_table>
# LEFT JOIN <right_table> ON <left_table>.<common_column> = <right_table>.<common_column>

df = pd.read_sql(
    """
    SELECT a.date, a.team, a.opp, a.first, a.last
    FROM
        (SELECT game_id, date, home as team, away as opp, player_id, player.name, last, first
        FROM game, player
        WHERE
            game.home = player.team
        UNION
        SELECT game_id, date, home as team, away as opp, player_id, player.name, last, first
        FROM game, player
        WHERE
            game.away = player.team) AS a
    LEFT JOIN player_game AS b ON a.game_id = b.game_id AND a.player_id = b.player_id
    """, conn)

df.query("last == 'Redick'")

df = pd.read_sql(
    """
    SELECT game_id, home as team, first, last
    FROM game, player
    WHERE
        game.home = player.team
    UNION
    SELECT game_id, home as team, first, last
    FROM game, player
    WHERE
        game.away = player.team
    """, conn)


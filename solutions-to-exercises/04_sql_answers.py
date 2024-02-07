"""
Answers to the end of chapter exercises for SQL chapter.

Note: this assumes you've already created/populated the SQL database as
outlined in the book and ./code/04_sql.py.
"""
import pandas as pd
from os import path
import sqlite3

DATA_DIR = './data'

conn = sqlite3.connect(path.join(DATA_DIR, 'basketball-data.sqlite'))

###############################################################################
# 4.1
###############################################################################
df  = pd.read_sql(
    """
    SELECT date, name, fgm, fga, pts AS points
    FROM player_game, team
    WHERE team.team = player_game.team AND
    team.division = 'Central'
    """, conn)

###############################################################################
# 4.2
###############################################################################
df  = pd.read_sql(
    """
    SELECT p.first, p.last, date, fgm, fga, pts AS points
    FROM player_game AS pg, team AS t, player AS p
    WHERE t.team = pg.team AND
    t.division = 'Central' AND p.player_id = pg.player_id
    """, conn)

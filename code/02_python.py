##############
# basic python
##############

##########################
# how to read this chapter
##########################
1 + 1

##########
# comments
##########

# print the result of 1 + 1
print(1 + 1)

###########
# variables
###########

three_pt_made = 4

three_pt_made
3*three_pt_made

three_pt_made = three_pt_made + 1

three_pt_made

####################
# types of variables
####################

over_under = 216  # int
fg_percentage = 0.48  # float

starting_c = 'Karl-Anthony Towns'
starting_pg = "D'Angelo Russel"

type(starting_c)

type(over_under)

starters = f'{starting_c}, {starting_pg}, etc.'
starters

# string methods
'from downtown!'.upper()

'Ron Artest'.replace('Artest', 'World Peace')

####################################
# How to figure things out in Python
####################################
'lebron james'.capitalize()

'  lebron james'
'lebron james'

#######
# bools
#######
team1_pts = 110
team2_pts = 120

# and these are all bools:
team1_won = team1_pts > team2_pts
team2_won = team1_pts < team2_pts
teams_tied = team1_pts == team2_pts
teams_did_not_tie = team1_pts != team2_pts

type(team1_won)
teams_did_not_tie

# error because test for equality is ==, not =
# teams_tied = (team1_pts = team2_pts)  # commented out since it throws an error

shootout = (team1_pts > 130) and (team2_pts > 130)
at_least_one_good_team = (team1_pts > 120) or (team2_pts > 120)
you_guys_are_bad = not ((team1_pts > 100) or (team2_pts > 100))
meh = not (shootout or at_least_one_good_team or you_guys_are_bad)

###############
# if statements
###############
if team1_won:
  message = "Nice job team 1!"
elif team2_won:
  message = "Way to go team 2!!"
else:
  message = "must have tied!"

message

#################
# container types
#################

# lists
roster_list = ['kevin durant', 'kyrie irving', 'james harden']

roster_list[0]
roster_list[0:2]
roster_list[-2:]

# dicts
roster_dict = {'PF': 'kevin durant',
               'SG': 'kyrie irving',
               'PG': 'james harden'}

roster_dict['PF']
roster_dict['C'] = 'deandre jordan'

# unpacking
sg, pg = ['kyrie irving', 'james harden']

sg = 'kyrie irving'
pg = 'james harden'

# gives an error - n of variables doesn't match n items in list
# sg, pg = ['kevin durant', 'kyrie irving', 'james harden']  # commented out w/ error

#######
# loops
#######

# looping over a list
roster_list = ['kevin durant', 'james harden', 'kyrie irving']

roster_list_upper = ['', '', '']
i = 0
for player in roster_list:
    roster_list_upper[i] = player.title()
    i = i + 1

roster_list_upper

for x in roster_dict:
    print(f"position: {x}")

for x in roster_dict:
   print(f"position: {x}")
   print(f"player: {roster_dict[x]}")

for x, y in roster_dict.items():
    print(f"position: {x}")
    print(f"player: {y}")

################
# comprehensions
################

# lists
roster_list
roster_list_proper = [x.title() for x in roster_list]
roster_list_proper

roster_list_proper_alt = [y.title() for y in roster_list]

type([x.title() for x in roster_list])
[x.title() for x in roster_list][:2]

roster_last_names = [full_name.split(' ')[1] for full_name in roster_list]
roster_last_names

full_name = 'kevin durant'
full_name.split(' ')
full_name.split(' ')[1]

roster_k_only = [
    x for x in roster_list if x.startswith('k')]
roster_k_only

roster_k_only_title = [
    x.title() for x in roster_list if x.startswith('k')]
roster_k_only_title

# dicts
salary_per_player = {
    'kevin durant': 39058950, 'kyrie irving': 33460350, 'james harden': 41254920}

salary_m_per_upper_player = {
    name.upper(): salary/1000000 for name, salary in salary_per_player.items()}

salary_m_per_upper_player

sum([1, 2, 3])

sum([salary for _, salary in salary_per_player.items()])

###########
# functions
###########
len(['kevin durant', 'james harden', 'kyrie irving'])

def pts(fg2, fg3, ft):
    """
    multi line strings in python are between three double quotes

    it's not required, but the convention is to put what the fn does in one of these multi line strings (called "docstring") right away in function

    this function takes number of 2 point fgs, 3 point fgs, and free throws and
    returns total points scored
    """
    return fg2*2 + fg3*3 + ft*1

pts(8, 4, 5)

# this gives an error: fg2 is only defined inside pts
# print(fg2)

def pts_noisy(fg2, fg3, ft):
    """
    this function takes number of 2 point fgs, 3 point fgs, and free throws and
    returns total points scored

    it also prints out fg2
    """
    print(fg2)  # works here since we're inside fn
    return fg2*2 + fg3*3 + ft*1

pts_noisy(8, 4, 5)

# side effects
def is_player_on_team(player, team):
    """
    take a player string and team list and check whether the player is on team

    do this by adding the player to the team, then returning True if the player shows up 2 or more times
    """
    team.append(player)
    return team.count(player) >= 2

roster_list = ['kevin durant', 'james harden', 'kyrie irving']
is_player_on_team('jared dudley', roster_list)

roster_list
is_player_on_team('jared dudley', roster_list)

roster_list

#############################
# default values in functions
#############################

# error: leaving off a an argument
# pts(4, 2)

def pts_w_default(fg2=0, fg3=0, ft=0):
    """
    this function takes number of 2 point fgs, 3 point fgs, and free throws and
    returns total points scored
    """
    return fg2*2 + fg3*3 + ft*1

pts_w_default(4, 2)
pts_w_default()

def pts2(fg2=0, fg3=0, ft=0, pts_per_3=3):
    """
    takes number of receiving: yards, receptions and touchdowns AND points per
    reception and returns fantasy points scored
    """
    return fg2*2 + fg3*pts_per_3 + ft*1

pts2(4, 2, 2)  # not doing what we want

4*2 + 4*1 + 0.5*6

pts2(4, 2, 0, 2)  # solution 1
pts2(4, 2, pts_per_3=2)  # solution 2

# error: can't put key word argument before positional
# pts2(pts_per_3=2, 4, 2)

#####################################
# functions that take other functions
#####################################

def do_to_list(working_list, working_fn, desc):
    """
    this function takes a list, a function that works on a list, and a
    description

    it applies the function to the list, then returns the result along with
    description as a string
    """

    value = working_fn(working_list)

    return f'{desc} {value}'

def last_elem_in_list(working_list):
    """
    returns the last element of a list.
    """
    return working_list[-1]

positions = ['C', 'PF', 'SF', 'SG', 'PG']

do_to_list(positions, last_elem_in_list, "last element in your list:")
do_to_list([1, 2, 4, 8], last_elem_in_list, "last element in your list:")

do_to_list(positions, len, "length of your list:")

do_to_list([2, 3, 7, 1.3, 5], lambda x: 3*x[0], "first element in your list times 3 is:")

# normally imports like this would be at the top of the file
import os

os.cpu_count()

from os import path

# change this to the location of your data
DATA_DIR = '/Users/nathan/nba-book/data'
path.join(DATA_DIR, 'adp_2017.csv')
os.path.join(DATA_DIR, 'adp_2017.csv')  # alt if we didn't want to import path

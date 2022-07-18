"""
Answers to the end of chapter exercises for Python chapter.

Questions with written (not code) answers are inside triple quotes.
"""

###############################################################################
# 2.1
###############################################################################
"""
a) `_throwaway_data`. Valid. Python programmers often start variables with `_`
   if they're throwaway or temporary, short term variables.
b) `n_shots`. Valid.
c) `3_pt_percentage`. Not valid. Can't start with a number.
d) `numOfBoards`. Valid, though convention is to split words with `_`, not camelCase.
e) `flagrant2`. Valid. Numbers OK as long as they're not in the first spot
f) `coach name`. Not valid. No spaces
g) `@home_or_away`. Not valid. Only non alphanumeric character allowed is `_`
h) `'ft_attempts'`. Not valid. A string (wrapped in quotes), not a variable
   name. Again, only non alphanumeric character allowed is `_`
"""

###############################################################################
# 2.2
###############################################################################
weekly_points = 100
weekly_points = weekly_points + 28
weekly_points = weekly_points + 5

weekly_points # 133

###############################################################################
# 2.3
###############################################################################
def commentary(player, play):
    return f'{player} with the {play}!'

commentary('Lebron', 'dunk')

###############################################################################
# 2.4
###############################################################################
"""
It's a string method, so what might `islower()` in the context of a string?
I'd say it probably returns whether or not the string is lowercase.

A function "is *something*" usually returns a yes or no answer (is it
something or not), which would mean it returns a boolean.

We can test it like:
"""

'lebron james'.islower()  # should return True
'Lebron James'.islower()  # should return False

###############################################################################
# 2.5
###############################################################################
def is_fox(player):
    return player.replace("'", '').lower() == 'deaaron fox'

is_fox('lebron james')
is_fox("De'Aaron Fox")
is_fox("DEAARON FOX")

###############################################################################
# 2.6
###############################################################################
def is_good_score(score):
    if score >= 100:
        return f'{score} is a good score'
    else:
        return f"{score}'s not that good"

commentary(90)
commentary(130)

###############################################################################
# 2.7
###############################################################################
roster = ['kevin durant', 'kyrie irving', 'james harden']

roster[0:2]
roster[:2]
roster[:-1]
[x for x in roster if x != 'james harden']
[x for x in roster if not x.startswith('j')]
[x for x in roster if x in ['kevin durant', 'kyrie irving']]

###############################################################################
# 2.8
###############################################################################
shot_info = {'shooter': 'Steph Curry', 'is_3pt': True, 'went_in': False}

# a
shot_info['shooter'] = 'Devon Booker'
shot_info

# b
def toggle3(info):
    info['is_3pt'] = not info['is_3pt']
    return info

toggle3(shot_info)

###############################################################################
# 2.9
###############################################################################
"""
a) No. `'is_ft'` hasn't been defined.
b) No, `shooter` is a variable that hasn't been defined, the key is
`'shooter'`.
c) Yes.
"""

###############################################################################
# 2.10
###############################################################################
roster = ['kevin durant', 'kyrie irving', 'james harden']

# a
for x in roster:
  print(x.split(' ')[-1])

# b
{player: len(player) for player in roster}

###############################################################################
# 2.11
###############################################################################
roster_dict = {'PF': 'kevin durant',
               'SG': 'kyrie irving',
               'PG': 'james harden',
               'C': 'deandre jordan'}

# a
[pos for pos in roster_dict]

# b
[player for _, player in roster_dict.items()
    if player.split(' ')[-1][0] in ['h', 'j']]

###############################################################################
# 2.12
###############################################################################
# a
def mapper(my_list, my_function):
  return [my_function(x) for x in my_list]

# b
list_of_n_3pt_made = [5, 6, 1, 0, 4, 4]

mapper(list_of_n_3pt_made, lambda x: x*3)

# ---------------------------------------------------------------------------- #
# World Cup: TrueSkill Results
# Ver: 0.01
# ---------------------------------------------------------------------------- #
#
# 1. run trueskill_match.py to get probabilities
# 2. run trueskill results to update rating and print results sheet
#
# ---------------------------------------------------------------------------- #

import pandas as pd
import datetime as dt

# ---------------------------------------------------------------------------- #

# After game parameters
Ascore = 1
Bscore = 2

# ---------------------------------------------------------------------------- #

# get match data
# os.chdir('C:/Users/Marc Gumowski/Documents/GitHub/WorldCup2018TrueSkill')
os.chdir('C:/Users/Gumistar/Documents/GitHub/WorldCup2018TrueSkill')
execfile('py/trueskill_match.py')

# get latest results
# os.chdir('C:/Users/Marc Gumowski/Documents/GitHub/WorldCup2018TrueSkill')
os.chdir('C:/Users/Gumistar/Documents/GitHub/WorldCup2018TrueSkill')
results = pd.read_csv('csv/results.csv')

# append results
if Ascore > Bscore:
    Awin = 1
    Arank = 0
    Brank = 1
elif Ascore < Bscore:
    Awin = 0
    Arank = 1
    Brank = 0
else:
    Awin = 0.5
    Arank = 0
    Brank = 0

new_results = {'id': match_id,
     'Ateam': Ateam,
     'BTeam': Bteam,
     'Ascore': Ascore,
     'Bscore': Bscore,
     'Awin': Awin}
results = results.append(new_results, ignore_index = True)

# Compute new rates
new_rate = trueskill.rate([Acomp, Bcomp], [Arank, Brank])
for i, team in enumerate([Ateam, Bteam]):
    for player in new_rate[i].keys():
        rating[team][player] = new_rate[i][player]

# save
results.to_csv('csv/results.csv', index = False)
np.save('npy/TrueSkill_Rating_' + dt.datetime.now().strftime("%d_%m_%Y") + "_AfterGame" + match_id + '.npy', rating)
# ---------------------------------------------------------------------------- #
# World Cup: TrueSkill Match
# Ver: 0.01
# ---------------------------------------------------------------------------- #
#
# Winning probabilities for each match-up
#
# ---------------------------------------------------------------------------- #

import numpy as np
import pandas as pd
import datetime as dt
import os
import trueskill
import math
import matplotlib.pyplot as plt

# match-up parameter
match_id = '3'
Ateam = "Morocco"
Bteam = "Iran"

# TrueSkill parameters
scale = [0, 10]
mu = 6
sigma = mu / 3
env = trueskill.TrueSkill(mu = mu, sigma = sigma)
env.create_rating()

# get latest rating
os.chdir('C:/Users/Gumistar/Documents/GitHub/WorldCup2018TrueSkill/npy')
latest_rating = max(os.listdir(os.getcwd()), key = os.path.getmtime)
rating = np.load(latest_rating).item()

# match-up
Acomp = rating[Ateam]
Bcomp = rating[Bteam]

# win prob
def win_probability(Acomp, Bcomp, env = trueskill.global_env()):
    delta_mu = sum(Acomp[r].mu for r in Acomp.keys()) - sum(Bcomp[r].mu for r in Bcomp.keys())
    sum_sigma = sum(Acomp[r].sigma ** 2 for r in Acomp.keys()) + sum(Bcomp[r].sigma ** 2 for r in Bcomp.keys())
    size = len(Acomp) + len(Bcomp)
    denom = math.sqrt(size * (env.beta * env.beta) + sum_sigma)
    ts = env
    return ts.cdf(delta_mu / denom)
win_prob = win_probability(Acomp, Bcomp, env)
print(Ateam + ' winning probability is ' + str(round(win_prob * 100, 2)) + "%")
print(Bteam + ' winning probability is ' + str(round((1 - win_prob) * 100, 2)) + "%")

# plot
height = [win_prob, 1 - win_prob]
bars = (Ateam, Bteam)
y_pos = np.arange(len(bars))
plt.bar(y_pos, height, color = ("#DE7A22", "#6AB187"))
plt.title('Match-up winning probabilities based on TrueSkill rating')
plt.xlabel('team')
plt.ylabel('prob')
plt.ylim(0, 1)
plt.xticks(y_pos, bars)
plt.show()

# ---------------------------------------------------------------------------- #

# After game parameters
Ascore = 0
Bscore = 1

# get latest results
os.chdir('C:/Users/Gumistar/Documents/GitHub/WorldCup2018TrueSkill')
results = pd.read_csv('csv/results.csv')

# Compute new rates
new_rate = trueskill.rate([Acomp, Bcomp], [0, 0])
for i, team in enumerate([Ateam, Bteam]):
    for player in new_rate[i].keys():
        rating[team][player] = new_rate[i][player]

# append results
if Ascore > Bscore:
    Awin = 1
elif Ascore < Bscore:
    Awin = 0
else:
    Awin = 0.5
new_results = {'id': match_id,
     'Ateam': Ateam,
     'BTeam': Bteam,
     'Ascore': Ascore,
     'Bscore': Bscore,
     'Awin': Awin}
results = results.append(new_results, ignore_index = True)

# save
results.to_csv('csv/results.csv', index = False)
np.save('npy/TrueSkill_Rating_' + dt.datetime.now().strftime("%d_%m_%Y") + "_Game" + match_id + '.npy', rating)
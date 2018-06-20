# ---------------------------------------------------------------------------- #
# World Cup: TrueSkill Match
# Ver: 0.01
# ---------------------------------------------------------------------------- #
#
# Winning probabilities for each match-up
#
# ---------------------------------------------------------------------------- #

import numpy as np
import os
import re
import trueskill
import math
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------- #

# match-up parameter
match_id = '20' # 20 Iran Spain
Ateam = "Iran"
Bteam = "Spain"

# ---------------------------------------------------------------------------- #

# TrueSkill parameters
scale = [0, 10]
mu = 6
sigma = mu / 3
env = trueskill.TrueSkill(mu = mu, sigma = sigma)
env.create_rating()

# get latest rating
os.chdir('C:/Users/Marc Gumowski/Documents/GitHub/WorldCup2018TrueSkill/npy')
# os.chdir('C:/Users/Gumistar/Documents/GitHub/WorldCup2018TrueSkill/npy')
latest_rating = max(os.listdir(os.getcwd()), key = os.path.getmtime)
# control id not to predict in-sample
control = re.search('[^._]+(?=[^_]*$)', latest_rating)[0]
control = re.sub('[^0-9]', '', control)
if int(control) == int(match_id):
    latest_rating = max(sorted(os.listdir(os.getcwd()), key = os.path.getmtime)[:-1], key = os.path.getmtime)
rating = np.load(latest_rating).item()

# match-up
Acomp = rating[Ateam]
Bcomp = rating[Bteam]

# Awin prob
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

# draw prob
print('{:0.1%} chance to draw'.format(trueskill.quality([Acomp, Bcomp])))

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



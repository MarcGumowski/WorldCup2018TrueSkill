import numpy as np
import os
import trueskill
import math

# TrueSkill parameters
scale = [0, 10]
mu = 6
sigma = mu / 3
env = trueskill.TrueSkill(mu = mu, sigma = sigma)
env.create_rating()

# get data
os.chdir("C:/Users\Marc Gumowski/Documents/GitHub/WorldCup2018TrueSkill")
rating = np.load("npy/rating_dict.npy").item()

# clean
for team in rating.keys():
    for player in rating[team].keys():
        rating[team][player] = float(rating[team][player])

def replace_rating(x, old_value, new_value):
    for xkey in x.keys():
        for ykey in x[xkey].keys():
            if x[xkey][ykey] == old_value:
                x[xkey][ykey] = new_value

replace_rating(rating, 0, mu)
replace_rating(rating, np.nan, mu)

# trueskill rating for each player
def replace_in_dict(dictionnary, func):
    return {team : {player : func(dictionnary[team][player]) for player in dictionnary[team].keys()} for team in dictionnary.keys()}
rating = replace_in_dict(rating, env.Rating)

# prob
Ateam = "Russia"
Bteam = "Saudi Arabia"
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
win_probability(Acomp, Bcomp, env)

# Compute new rates
new_rate = trueskill.rate([Acomp, Bcomp], [1, 0])
for i, team in enumerate([Ateam, Bteam]):
    for player in new_rate[i].keys():
        rating[team][player] = new_rate[i][player]





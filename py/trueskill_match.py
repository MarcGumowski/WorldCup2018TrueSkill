import numpy as np
import datetime as dt
import os
import trueskill

# get latest rating
os.chdir("C:/Users\Marc Gumowski/Documents/GitHub/WorldCup2018TrueSkill/npy")
latest_rating = max(os.listdir(os.getcwd()), key = os.path.getmtime)
rating = np.load(latest_rating).item()

# matchup
Ateam = "Egypt"
Bteam = "Uruguay"
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
new_rate = trueskill.rate([Acomp, Bcomp], [0, 1])
for i, team in enumerate([Ateam, Bteam]):
    for player in new_rate[i].keys():
        rating[team][player] = new_rate[i][player]

 # np.save('TrueSkill_Rating_' + dt.datetime.now().strftime("%d_%m_%Y_%Hh%M") + '.npy', rating)
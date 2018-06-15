import numpy as np
import os
import trueskill

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

np.save('npy/TrueSkill_Rating_Start.npy', rating)





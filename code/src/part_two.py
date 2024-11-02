import pandas as pd
from player import Player

def calculate_mean_median_std(players, category):
    filtered_players = list(filter(lambda x: str(x.stats[category]) != 'N/a' , players))
    players = filtered_players    
    mean = sum([float(player.stats[category]) for player in players]) / len(players)
    median = sorted([float(player.stats[category]) for player in players])[len(players)//2]
    std = (sum([(float(player.stats[category]) - mean)**2 for player in players]) / len(players))**0.5
    return mean, median, std

def find_top_3(players, reverse=False, keyword='worst'):
    f = open('./output/top_3_'+ keyword +'_players.txt', 'w', encoding='utf-8')
    f.write('Top 3 '+ keyword +' players in each category:\n\n'.upper())
    
    for category in categories:
        filtered_players = list(filter(lambda x: x.stats[category] != 'N/a' , players))
        players_ = sorted(filtered_players, key=lambda x: (x.stats[category]), reverse=reverse)
        f.write(f'Top 3 players in {category}:\n')
        
        for i in range(3):
            f.write(f'{i+1}. {players_[i].stats["player"]: <50} : {players_[i].stats[category]}\n')
        f.write('\n')

# =============================================================================================

# Read data from './output/result.csv'
data = pd.read_csv('./output/result.csv')

# Parse data into Player objects
categories = list(data.columns)
players = []
for index, row in data.iterrows():
    player = Player(row.to_dict())
    for key in player.stats:
        if key in categories:
            player.stats[key] = row[key]
    players.append(player)

# Find top 3 best players in each category
for category in ['player', 'nationality', 'position', 'team', 'age', 'birth_year']:
    categories.remove(category)

# for i in range(len(players)):
#     print(players[i].stats['aerials_won_pct'])

find_top_3(players, reverse=True, keyword='best')
find_top_3(players, reverse=False, keyword='worst')

# =============================================================================================

teams = set()
for player in players:
    teams.add(player.stats['team'])

# find mean, median, standard deviation of each category
# write to result2.csv with each column are mean, median, standard deviation of 
# each category respectively
# for all players and each team
# mean of atrribute1, median of attribute1, std of attribute1

labels = ['mean', 'median', 'std']
headers =  ['']

for category in categories:
    for label in labels:
        headers.append(label + ' of ' + category)

tables = []

# mean, median, std of all players
data = ['all']
for category in categories:
    mean, median, std = calculate_mean_median_std(players, category)
    data.extend([mean, median, std])
tables.append(data)

for team in sorted(teams):
    row = [team]
    team_players = list(filter(lambda x: x.stats['team'] == team, players))
    for category in categories:
        mean, median, std = calculate_mean_median_std(team_players, category)
        row.extend([mean, median, std])
    tables.append(row)

# row 1: median, mean, std of all players
# row 2+: median, mean, std of each team
dataframe = pd.DataFrame(tables, columns=headers)
dataframe.to_csv('./output/result2.csv', index=True)

# =============================================================================================
# Plotting histogram of each category for all players
import matplotlib.pyplot as plt
import os

if not os.path.exists('../images'):
    os.mkdir('../images/all')
for category in categories:
    values = [float(player.stats[category]) for player in players if player.stats[category] != 'N/a']
    plt.hist(values, bins=20)
    plt.title('Histogram of ' + category)
    plt.xlabel(category)
    plt.ylabel('Frequency')
    plt.savefig('../images/all/histogram_' + category + '.png')
    plt.clf()

for team in sorted(teams):
    if not os.path.exists('../images/' + team):
        os.mkdir('../images/' + team)
    for category in categories:
        values = [float(player.stats[category]) for player in players if player.stats['team'] == team and player.stats[category] != 'N/a']
        plt.hist(values, bins=20)
        plt.title('Histogram of ' + category + ' for ' + team)
        plt.xlabel(category)
        plt.ylabel('Frequency')
        plt.savefig('../images/' + team  + '/histogram_' + team + '_' + category + '.png')
        plt.clf()

# =============================================================================================
# Find best team in each category
f = open('./output/best_team_in_each_category.txt', 'w', encoding='utf-8')
f.write('Best team in each category:\n\n'.upper())
freq = {}
for category in categories:
    max_mean = 0
    best_team = ''
    for team in sorted(teams):
        team_players = list(filter(lambda x: x.stats['team'] == team, players))
        mean, _, _ = calculate_mean_median_std(team_players, category)
        if mean > max_mean:
            max_mean = mean
            best_team = team
    
    f.write(f'Best team in {category: <35}: {best_team: <20} : mean = {max_mean: .4f}\n')
    if best_team in freq:
        freq[best_team] += 1
    else:
        freq[best_team] = 1
f.close()

print("Best team of the season is " + max(freq, key=freq.get))
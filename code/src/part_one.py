'''
=====================================
    Author: Duong Phan Bao Linh     |
    StudentID: B22DCCN485           |
=====================================
'''


from player import Player
import tools
import requests
import pandas as pd

'''
    TODO:
    - get data-stat from each category
    - get assigned value for each data-stat
    - give output at 'result.csv'
'''

URL = 'https://fbref.com/en/comps/9/2023-2024/'
categories = [
    'stats',
    'keepers',
    'shooting',
    'passing',
    'passing_types',
    'gca', # goal and shot creation
    'defense',
    'possession',
    'playingtime',
    'misc'
]
dest = '2023-2024-Premier-League-Stats'
# Request and get data from URL
# scrapper = tools.Scrapper(URL, categories, dest)
# scrapper.scrap_and_export()

# Parse data from HTML files
parser = tools.Parser(categories, dest)
player_list = parser.parse_player()

# Filter out players with played minutes less than 90
player_list = list(filter(lambda x: x.stats['minutes'] != 'N/a' 
                          and int(x.stats['minutes']) >= 90, player_list))

# Sort players by name, if same name, sort by age
player_list.sort(key=lambda x: (x.stats['player'], x.stats['age']))

# Export to CSV        
parser.to_csv(player_list)
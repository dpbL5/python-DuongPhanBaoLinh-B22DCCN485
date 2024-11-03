from bs4 import BeautifulSoup as bs
from bs4 import Comment
from player import Player
import pandas as pd
import requests
import os

class Scrapper:
    def __init__(self, url, folders, dest):
        self.url = url
        self.folders = folders # list of strings
        self.dest = dest
        
    def scrap_and_export(self):
        
        if not os.path.exists('./code/exports'):
            os.makedirs('./code/exports')
            
        for folder in self.folders:
            html_export = open('./code/exports/' + folder + '.html', 'a', encoding='utf-8')
            URL = self.url + '/' + folder + '/' + self.dest
            response = requests.get(URL).content
            soup = bs(response, 'lxml')
            freezed = soup.find_all(string=lambda text: isinstance(text, Comment))
            for block in freezed:
                if 'table' in block:
                    html_export.write(block)

class Parser:
    def __init__(self, folders, dest):
        self.folders:list = folders
        self.dest = dest
     
    def parse_player(self) -> list[Player]:
        # stats_var : Name of the stats
        stats_vars = dict()
        
        # Get stats variables
        for category in self.folders:
        # for category in ['stats']:
            source = open('./code/exports/' + category + '.html', 'r', encoding='utf-8')
            soup = bs(source, 'lxml')
            rows = soup.find_all('tr', limit=2) # only need the first two rows
            for cell in rows[1].find_all('th'):
                if (cell.get('data-stat') is not None):
                    stats_vars[cell.get('data-stat')] = cell.text
        stats_vars.pop('ranker', None)
        stats_vars.pop('matches', None)
            
        # Assign all player stats
        player_list = dict()
        for category in self.folders:
        # for category in ['shooting']:
            source = open('./code/exports/' + category + '.html', 'r', encoding='utf-8')
            soup = bs(source, 'lxml')
            rows = soup.find_all('tr')[2:] # skip the first and second rows
            for row in rows:
                # Check if the player is already in the list
                if row.find('td', {'data-append-csv': True}) is None: continue
                id = row.find('td', {'data-append-csv': True}).get('data-append-csv')
                
                if player_list.get(id) is None:
                    # create new player
                    player = Player(stats_vars)
                    for cell in row.find_all('td'):
                        if cell.get('data-stat') in stats_vars:
                            if cell.get('csk') is not None:
                                #special case for position
                                if cell.get('data-stat') == 'position':
                                    player.stats[cell.get('data-stat')] = cell.text
                                else: player.stats[cell.get('data-stat')] = cell.get('csk')
                            else: player.stats[cell.get('data-stat')] = 'N/a' if cell.text == '' else cell.text
                    player_list[id] = player
                else: # update player stats
                    for cell in row.find_all('td'):
                        if cell.get('data-stat') in stats_vars:
                            if cell.get('csk') is not None:
                                if cell.get('data-stat') == 'position':
                                    player.stats[cell.get('data-stat')] = cell.text
                                else: player_list[id].stats[cell.get('data-stat')] = cell.get('csk')
                            else: player_list[id].stats[cell.get('data-stat')] = 'N/a' if cell.text == '' else cell.text

        refine_player_list = []
        for player in player_list.values():
            refine_player_list.append(player)
        return refine_player_list
                    
    
    # export to csv
    def to_csv(self, player_list):
        if not os.path.exists('./code/output'):
            os.makedirs('./code/output')
        player_list_data = []
        for player in player_list:
            player_list_data.append(list(player.stats.values()))
        data_frame = pd.DataFrame(player_list_data, columns=list(player_list[0].stats.keys()))
        data_frame.to_csv('./code/output/result.csv', index=False)
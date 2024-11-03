import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
import csv

sys.stdout.reconfigure(encoding='utf-8')

if __name__ == "__main__":
    url = 'https://www.footballtransfers.com/us/leagues-cups/national/uk/premier-league/2023-2024'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    table = soup.find('table', {
        'class': 'table table-striped table-hover leaguetable mvp-table ranking-table mb-0'
    })

    teams_data = [] 

    if table:
        tbody = table.find('tbody')
        if tbody:
            teams = tbody.find_all('a', href=True)

            for team in teams:
                teams_data.append([team.text.strip(), team['href']])

        else:
            raise Exception('no tbody')
    else:
        raise Exception('no table')
    
    players_data = []

    for team in teams_data:
        team_name = team[0]
        team_url = team[1]

        r_tmp = requests.get(team_url)
        soup_tmp = BeautifulSoup(r_tmp.text, 'html.parser')
        
        table_tmp = soup_tmp.find('table', {
            'class': 'table table-striped-rowspan ft-table mb-0'
        })

        if  table_tmp:
            tbody_tmp = table_tmp.find('tbody')
            if tbody_tmp:
                players = tbody_tmp.find_all('tr')

                for player in players:
                    if "odd" in player['class'] or "even" in player['class']:
                        player_name = player.find('th').find('span').get_text(strip = True)
                        player_cost = player.find_all('td')[-1].get_text(strip = True)
                        players_data.append([player_name, team_name,  player_cost])
                
            else:
                raise Exception('no tbody')
        else:
            raise Exception('no table')

    df = pd.DataFrame(players_data, columns=['Player', 'Team', 'Cost'])
    df.to_csv("./code/output/result4.csv", index=False, encoding='utf-8-sig')
    
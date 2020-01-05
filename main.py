from bs4 import BeautifulSoup
import requests 
import pandas as pd

base_url = 'https://pt.wikipedia.org/wiki/World_Soccer' 

# Send get http request
page = requests.get(base_url)

# Verify we had a successful get request webpage call
if page.status_code == requests.codes.ok:
    # Get the whole webpage in beautifulsoup 
    bs = BeautifulSoup(page.text, 'html.parser')

list_all_players = []
contador = 0

for ultag in bs.find_all('ul'):
    if(contador == 3):
        #list_all_players.append(ultag.text)
        list_all_players = ultag.find_all('li')
        break 
    else:
        contador += 1

last_ten_player = list_all_players[-10:]

data = {
    'Year': [],
    'Country': [], 
    'Player': [],
    'Team': []
}

for ltp in last_ten_player:
    data['Year'].append(ltp.find_all('a')[0].text)
    data['Country'].append(ltp.find_all('a')[1]['title'])
    data['Player'].append(ltp.find_all('a')[2].text)
    data['Team'].append(ltp.find_all('a')[3].text)


table = pd.DataFrame(data, columns=['Year', 'Country', 'Player', 'Team'])
table.index = table.index + 1
print(table)
table.to_csv('players_of_the_year.csv', sep=',', index=False, encoding='UTF-8')
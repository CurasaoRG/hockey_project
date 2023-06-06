import requests
from bs4 import BeautifulSoup
import csv
import time

# функция для извлечения данных о игроке
def extract_player_data(player):
    data = [td.text.strip() for td in player if td.text.strip()]
    number, full_name, age, born, birthplace, height, weight, stick = data
    name = full_name[:full_name.find('(')].strip()
    position = full_name[full_name.find('(')+1:full_name.find(')')].strip()
    captain = full_name[full_name.find(')')+1:-1].strip() if full_name[full_name.find(')')+1:-1].strip() else None
    return name, number, position, captain, born, birthplace, age, height, weight, stick

# функция для извлечения списка игроков из страницы команды
def extract_team_roster(team_roster_link):
    team_roster_url = requests.get(team_roster_link)
    soup = BeautifulSoup(team_roster_url.content, 'html.parser')
    players = soup.select_one('#roster').select('tbody tr:not([class="title"])')
    return [extract_player_data(player) for player in players]

# функция для записи данных в csv-файл
def write_to_csv(data, filename, header):
    with open(filename, mode=('a','w')[header], newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if header:
            writer.writerow(['Team', 'Season', 'Player', 'Player_number', 'Position', 'Captain', 'Born', 'Birthplace', 'Age', 'Height', 'Weight', 'Stick'])
        writer.writerows(data)

def main():
    first = True
    # seasons = [f"{2000+i}-{2000+i+1}" for i in range(8, 23)]
    dataset_storage_link = '/home/rg/Documents/Study/hockey_project/test.csv'
    seasons = ['2008-2009',]
    for season in seasons:
        season_link = f"https://www.eliteprospects.com/league/khl/{season}"
        current_teams_url = requests.get(season_link)
        soup_teams = BeautifulSoup(current_teams_url.content, 'html.parser')
        team_links = soup_teams.select_one('[class="table standings table-sortable"]').select('.team')
        for link in team_links:
            team_name = link.text.strip()
            team_roster_link = link.a['href']
            # на случай, если линка нет
            if not team_roster_link:
                continue
            team_roster = extract_team_roster(team_roster_link)
    
            # записываем данные в csv-файл
            data = [[team_name, season] + list(player_data) for player_data in team_roster]
            write_to_csv(data, dataset_storage_link, first)
            first = False
            
            print(f'{team_name} {season} was loaded')
            time.sleep(1)


if __name__ == "__main__":
    main()
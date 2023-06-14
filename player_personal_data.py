# открываю CSV с игроками, собираю все ссылки на игроков
#     создаю словарь с именем игрока
#     прохожу по ссылке
#     нахожу таблицу с персональными данными
#     собираю данные в словарь
#     нахожу таблицу с наградами
#         дописать: что делать, если нет наград
#     добавляю в словарь награды
#     провожу через парсинг через модель pydantic
#     записываю словарь в CSV

import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
import csv
import time
from player_personal_data_model import Player, Stats
import timeit

PLAYERS_DATA_CSV_LOC = '/home/rg/Documents/Study/hockey_project/players_data.csv'
PLAYERS_PERSONAL_DATA_LOC = '/home/rg/Documents/Study/hockey_project/players_personal_data.csv'
PLAYERS_STATS_LOC = '/home/rg/Documents/Study/hockey_project/players_stats.csv'

def write_csv(model, file_loc, mode, headers=False):
    with open(file_loc, mode, newline='') as csvfile:
            fieldnames = list(model.__fields__.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if headers:
                writer.writeheader()
            writer.writerow(model.dict())


def write_csv_mult(rows, file_loc, mode, headers=False):
    with open(file_loc, mode, newline='') as csvfile:
        fieldnames = list(rows[0].__dict__.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if headers:
            writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def collect_awards(soup):
    awards = soup.select('div[id="awards"] li div[class^=col-xs]')
    player_awards = {}
    for tag in awards:
        lst = tag.select('li')
        if not lst:
            season = tag.text.strip()
        else:
            player_awards[season] = list(li.text.strip() for li in lst)
    return player_awards


def get_personal_data(soup):
        data = {}
        t3 = soup.select('.ep-card .ep-list__item')
        for tag in t3:
            lst = tag.find_all('div')
            data[lst[0].text.strip()] = lst[1].text.strip()
        return data

def main():

    df = pd.read_csv(PLAYERS_DATA_CSV_LOC)[['Player', 'Player_link']].drop_duplicates()
    try:
        loaded = pd.read_csv(PLAYERS_PERSONAL_DATA_LOC)['Player_link']
        # loaded = pd.read_csv(PLAYERS_PERSONAL_DATA_LOC)['Player_link'].shape[0]
    except FileNotFoundError:
        loaded = 0
    headers = not bool(loaded.shape[0])
    players = []
    rows = []
    for index, row in df.iterrows():
        player_name, player_link = row
        if player_link in list(loaded):
            continue
        data = requests.get(player_link)
        page = data.content
        soup = BeautifulSoup(page, 'html.parser')
        data_row = {'Player_name':player_name, 'Player_link':player_link}
        stats = soup.select('[class*="player-stats"] [class*="player-stats"]')
        for tag in stats:
            rows.append(Stats.from_tag(data_row, tag))
        data_row.update(get_personal_data(soup))
        data_row['Awards'] = json.dumps(collect_awards(soup))
        players.append(Player.from_dict(data_row))
        time.sleep(0.5)
        if index%10 == 0:
            write_csv_mult(players, PLAYERS_PERSONAL_DATA_LOC, mode = 'w' if headers else 'a', headers=headers)
            write_csv_mult(rows, PLAYERS_STATS_LOC, mode = 'w' if headers else 'a', headers=headers)
            players = []
            rows = []
            print(f"Loaded index {index} of {df.shape[0]}. Last player loaded: {player_name}.")
    else:
        write_csv_mult(players, PLAYERS_PERSONAL_DATA_LOC, mode = 'w' if headers else 'a', headers=headers)
        write_csv_mult(rows, PLAYERS_STATS_LOC, mode = 'w' if headers else 'a', headers=headers)
        print(f"Load complete")
if __name__ == "__main__":
    main()
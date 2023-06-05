import pandas as pd
import time

base_url = "https://www.eliteprospects.com/league/khl/"
dataset_storage_link = '/home/rg/Documents/Study/hockey_project/players_data.csv'
# first = True

def convert_string_to_tuple(line):
    # извлечение имени игрока и удаление пробелов в начале и конце
    name = line[:line.find('(')].strip()
    
    # извлечение позиции игрока
    position = line[line.find('(')+1:line.find(')')].strip()
    
    # извлечение символа капитана или реплики, если есть
    captain = line[line.find(')')+1:-1].strip()
    if not captain: captain=None
    # создание кортежа из полученных значений
    return [name, position, captain]

def main():
    first = True
    # строго говоря, нужно определять доступные сезоны по информации со страницы, пока так
    for i in range(8, 23):
        season = f"{2000+i}-{2000+i+1}"
        season_link = f"https://www.eliteprospects.com/league/khl/{season}"
        # извлекаю ссылки на список команд на данный сезон
        # можно добавить дополнительную верификацию на случай изменений на странице
        current_teams = pd.read_html(season_link, extract_links ='body')
        current_teams = current_teams[2]['Team']
        # обхожу команды 
        for item in current_teams:
            team_name = item[0]
            team_roster_link = item[1]
            # на случай, если линка нет
            if not team_roster_link:
                continue
            # читаю страницу с составом команды
            team_roster = pd.read_html(team_roster_link, extract_links ='body')
            team_roster = team_roster[2]
            # оставляю только нужные поля, извлекаю данные из кортежей
            team_roster = team_roster[['#', 'Player', 'A', 'Born', 'Birthplace', 'HT', 'WT', 'S']]
            team_roster = team_roster.drop(team_roster.index[-1])
            team_roster['Player_number'] = team_roster['#'].apply(lambda x: x[0][1:])
            team_roster['Age'] = team_roster['A'].apply(lambda x: x[0])
            team_roster['Born'] = team_roster['Born'].apply(lambda x: x[0])
            team_roster['Birthplace'] = team_roster['Birthplace'].apply(lambda x: x[0])
            # удаляю лишние строки, появившиеся из-за группировки в исходной таблице
            idx_to_drop = team_roster.loc[team_roster['Birthplace'].isin(['GOALTENDERS', 'DEFENSEMEN', 'FORWARDS'])].index
            team_roster = team_roster.drop(index=idx_to_drop)
            # продолжаю извлекать данные из кортежей
            team_roster['Height'] = team_roster['HT'].apply(lambda x: x[0])
            team_roster['Weight'] = team_roster['WT'].apply(lambda x: x[0])
            team_roster['Stick'] = team_roster['S'].apply(lambda x: x[0])
            # достаю ссылку на игрока
            team_roster[['Player', 'Player_link']] = team_roster['Player'].apply(lambda x: pd.Series([x[0], x[1]]))
            # разбиваю запись игрока на составляющие
            team_roster[['Player', 'Position', 'Captain']] = team_roster['Player'].apply(lambda x: pd.Series(convert_string_to_tuple(x)))
            # дописываю колонки с названием команды и сезоном
            team_roster['Team'] = team_name
            team_roster['Season'] = season
            # оставляю только нужные поля в нужном порядке
            team_roster = team_roster[['Team', 'Season', 
                                    'Player', 'Player_number','Position', 
                                    'Captain',
                                    'Born', 'Birthplace', 
                                    'Age', 'Height', 'Weight', 'Stick', 
                                    'Player_link'
                                    ]]
            # записываю в CSV, параметр first нужен для того, чтобы не дублировать заголовки
            team_roster.to_csv(dataset_storage_link, mode=('a','w')[first], header=first, index=False)
            first = False
            # показываю текущий прогресс и ожидаю 1 секунду, чтобы сервер не подумал чего
            print(f'{team_name} {season} was loaded')
            time.sleep(1)

if __name__ == "__main__":
    main()
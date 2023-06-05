import pandas as pd
import time
from eliteprospects_player_data_collection import convert_string_to_tuple

URL = "https://www.eliteprospects.com/transfers/confirmed?page="
dataset_location = "/home/rg/Documents/Study/hockey_project/transfers.csv"

def main():

    strange = []
# на случай, если не удалось загрузить с первого раза - открываю файл с инкрементом, 
# если файла нет - загружаем с начала
    try:
        with open(f'{dataset_location}_increment', 'r') as f:
            start_page = int(f.read())
    except FileNotFoundError:
        start_page = 1
    
    first = start_page==1
    last_page = 1672

    for i in range(start_page + 1,last_page + 1):
        datas = pd.read_html(URL+str(i),extract_links='body')
        if len(datas) > 2 and sum(datas[2].columns == ['DATE', 'STATUS', 'PLAYER', 'FROM', 'TO', 'SOURCE']) == 6:
            transfers = datas[2]
            # извлекаю данные из кортежей        
            transfers['Date'] = transfers['DATE'].apply(lambda x: x[0])
            transfers['Status'] = transfers['STATUS'].apply(lambda x: x[0])
            transfers[['Player', 'Player_link']] = transfers['PLAYER'].apply(lambda x: pd.Series([x[0], x[1]]))
            transfers[['From_team', 'From_team_link']] = transfers['FROM'].apply(lambda x: pd.Series([x[0], x[1]]))
            transfers[['To_team', 'To_team_link']] = transfers['TO'].apply(lambda x: pd.Series([x[0], x[1]]))
            transfers[['Player', 'Position']] = transfers['Player'].apply(lambda x: pd.Series(convert_string_to_tuple(x)[:2]))
            # удаляю технические строки 
            idx_to_drop = transfers.loc[transfers['Player_link'].isnull()].index
            transfers = transfers.drop(index=idx_to_drop)
            # оставляю только нужные колонки
            transfers[['Date', 'Player', 'Player_link', 'From_team', 'From_team_link','To_team', 'To_team_link']]\
                .to_csv(dataset_location, mode=('a','w')[first], header=first, index=False)
            time.sleep(0.5)
            # сохраняю номер последней удачно записанной страницы
            # строго говоря, могут появиться новые трансферы за время между запусками и тогда вся таблица поползет =:-[]
            with open(f'{dataset_location}_increment', 'w') as f:
                f.write(str(i))
            first = False
            # показываем текущие прогресс, и ожидаем 1 секунду, чтобы сервер не подумал, что его атакуют
            if i%25 == 0:
                print(f"Page {i} was loaded")
                time.sleep(1)
        else:
            # на случай странных ответов от сервера сохраняю все в резервный датасет
            strange.append(datas)
            for item in datas:
                item.to_csv(f"{dataset_location}.strange_from_page_{i}.csv", mode='a', header=True)
            print(f"{i}!",end="")


if __name__ == "__main__":
    main()
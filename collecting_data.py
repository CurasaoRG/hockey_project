import requests
from bs4 import BeautifulSoup
import csv
import sys

def get_links(soup, label):
    """
    вспомогательная процедура для получения списка ссылок с составами команд
    параметры запуска: 
        soup - объект BeautifulSoup для заданного сайта
        label - фильтр для сбора ссылок из разных выпадающих списков
    """
    links = []
    for optgroup in soup.find_all('optgroup'):
        if label in optgroup['label']:
            for option in optgroup.find_all('option'):
                    links.append(f"https://www.quanthockey.com/{option['value']}")
    return links[(label=='Seasons'):]

def get_team_n_season(soup):
    """
    вспомогательная процедура для получения названия команды и сезона
    """
    for sect in soup.find_all('section'):
        if sect.h1:
            team = sect.h1.get_text()
    team_name, season = team.replace('Roster @ KHL', '').split('  ')
    return team_name, season

def load_team_roster(url, file_name):
    """
    вспомогательная процедура для записи данных из таблиц на сайте в CSV-файл
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_ids = 'team-rosters-goalies', 'team-rosters-defensemen', 'team-rosters-forwards'
    team_name, season = get_team_n_season(soup)
    with open(file_name, 'a', newline='') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for table_id in table_ids:
            table = soup.find('table', {'id': table_id})
            for th in table.find('tbody'):
                for a in th.find_all('a'):
                    datawriter.writerow([team_name, season, a.get_text()])

def main():
    """
    процедура для сбора данных о составах команд с сайта https://www.quanthockey.com/
    входные параметры: имя файла для записи
    если имя файла не указано, то файл записывается по адресу: '/home/rg/Documents/Study/test/test.csv'
    """ 
    
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = '/home/rg/Documents/Study/test/test.csv'

    
    # URL страницы со списком игроков CSKA Москва
    url = "https://www.quanthockey.com/khl/team-rosters/cska-moscow-2022-23-khl-roster.html"

    # Получаем содержимое страницы
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # получаю ссылки на сезоны ЦСКА, текущий сезон отбрасываем, он уже открыт
    cska_links = get_links(soup, label='Seasons')[1:]
    
    # Собираю ссылки на составы остальных команд для текущего сезона
    teams_links = get_links(soup, label='Regular Season')

    # Собираю ссылки на составы для остальных сезонов, 
    # линки на ЦСКА там тоже будут, поэтому не загружаю данные для ЦСКА сразу
    for link in cska_links:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        teams_links += get_links(soup, label='Regular Season')
    
    # записываю составы команд в файл
    for link in teams_links:
        load_team_roster(url=link, file_name=file_name)

if __name__ == "__main__":
    main()
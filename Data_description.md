### players_data - данные игроков
    Team - команда
    Season - сезон
    Player - Имя игрока
    Player_number - игровой номер
    Position - игровое амплуа, возможные значения: 
        G - голкипер
        D - защитник
        RW - правый вингер
        LW - левый вингер
        C - центр-форвард
        F - форвард
        W - вингер
        сочетания через /
    Captain - статус игрока:
        C - капитан
        A - ассистент
    Born - год рождения
    Birthplace - место рождения
    Age - возраст на момент парсинга, 5 jun 2023
    Height - рост в см
    Weight - вес в кг
    Stick - хват клюшки
    Player_link - ссылка на страницу игрока, уникальное поле
### players_personal_data - дополнительные данные игроков
    Player_name - имя игрока
    Date_of_Birth - полная дата рождения
    Position - игровое амплуа, значения как в players_data
    Age - полных лет на момент выборки, 14 jun 23
    Place_of_Birth - место рождения, через запятую трёхбуквенное обозначение страны
    Nation - гражданство, если несколько, то перечислены через /
    Grip - хват клюшки
    Youth_Team - молодежная команда, в которой игрок начинал карьеру
    Height_cm - рост в см
    Height_ft - рост в футах
    Weight_kg - вес в кг
    Weight_lbs - вес в фунтах
    Awards - список наград по сезонам в формате JSON
    Player_link - ссылка на страницу игрока, уникальное поле
### transfers - переходы игроков
    Date - дата перехода
    Player - имя игрока
    Player_link - ссылка на страницу игрока
    From_team - старая команда
    From_team_link - ссылка на старую команду
    To_team - новая команда
    To_team_link - ссылка на новую команду
### players_stats - статистика игроков по сезонам
    Player_name - имя игрока
    Season - сезон
    Team - команда
    League - лига
    Player_link - ссылка на страницу игрока
    Регулярный сезон
        Regular_Games_Played - количество сыгранных игр
        Показатели только для полевых игроков (регулярный сезон)
            Regular_Goals - количество голов
            Regular_Assists - количество передач
            Regular_Total_Points - общее количество очков
            Regular_Penalty_Minutes - количество штрафных минут 
            Regular_Plus_Minus - показатель плюс-минус
        Показатели только для вратарей (регулярный сезон)
            Regular_Games_Dressed - количество игр, на которых вратарь был заявлен на игру, но сидел в запасе
            Regular_GAA - коэффициент надёжности, показывает, сколько в среднем шайб пропускает вратарь за 60 минут игрового времени
            Regular_Saves_Percentage - процент отраженных бросков
            Regular_Goals_Against - количество пропущенных голов
            Regular_Saves- количество сейвов
            Regular_Shutouts - количество игр на ноль
            Regular_WLT - соотношение выигранных, проигранных и ничейных (в основное время) игр
            Regular_TOI - время на льду
    Плей-офф (аналогично с регулярным сезоном)
        Postseason_Games_Played
        Показатели только для полевых игроков (плей-офф)
            Postseason_Goals
            Postseason_Assists
            Postseason_Total_Points
            Postseason_Penalty_Minutes
            Postseason_Plus_Minus
        Показатели только для вратарей (плей-офф)
            Postseason_Games_Dressed
            Postseason_GAA
            Postseason_Saves_Percentage
            Postseason_Goals_Against
            Postseason_Saves
            Postseason_Shutouts
            Postseason_WLT
            Postseason_TOI
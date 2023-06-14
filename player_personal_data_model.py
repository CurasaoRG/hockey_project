from typing import Optional
from pydantic import BaseModel
from dateutil.parser import parse
from datetime import datetime

class Player(BaseModel):
    Player_name:str
    Date_of_Birth: datetime
    Position: str
    Age: int|str
    Place_of_Birth: str
    Nation: str
    Grip: str
    Youth_Team: str
    Height_cm: Optional[int]
    Height_ft: Optional[str]
    Weight_kg: Optional[int]
    Weight_lbs: Optional[str]
    Awards: str
    Player_link: str

    @classmethod
    def from_dict(cls, data):
        dt = data.get('Date of Birth', '9999')
        height = data.get('Height', '')
        weight = data.get('Weight', '')

        Shoots=data.get('Shoots','')
        Catches = data.get('Catches','')
        grip = Shoots or Catches

        age = int(data['Age']) if data['Age'] else 'Deceased'
        # Parse Date of Birth field

        dt = parse(dt)

        # Parse height field
        height_cm, height_ft = parse_dim(height)

        # Parse weight field
        weight_kg, weight_lbs = parse_dim(weight)

        return cls(
            Player_name = data['Player_name'],
            Date_of_Birth=dt,
            Position=data['Position'],
            Age=age,
            Place_of_Birth=data['Place of Birth'],
            Nation=data['Nation'],
            Grip = grip,
            Youth_Team=data['Youth Team'],
            Height_cm=height_cm,
            Height_ft=height_ft,
            Weight_kg=weight_kg,
            Weight_lbs=weight_lbs,
            Awards = data['Awards'],
            Player_link = data['Player_link']
        )


def parse_dim(dim: str) -> tuple[Optional[int], Optional[str]]:
    if not dim:
        return None, None

    dim_parts = dim.split(' / ')
    dim_metric, dim_imperial = None, None
    if len(dim_parts) == 2:
        dim_metric_str, dim_imperial_str = dim_parts
        dim_metric = int(dim_metric_str.split(' ')[0])
        dim_imperial = dim_imperial_str.strip()
    else:
        dim_metric = int(dim.split(' ')[0])

    return dim_metric, dim_imperial


class Stats(BaseModel):
    Player_name:str
    Season: str
    Team: str
    League: Optional[str]
    Player_link: str
    # regular season
    Regular_Games_Played: Optional[int] # games played
    # field players only
    Regular_Goals: Optional[int] # goals
    Regular_Assists: Optional[int] # assists
    Regular_Total_Points: Optional[int] # points
    Regular_Penalty_Minutes: Optional[int] # penalty minutes
    Regular_Plus_Minus: Optional[int] # plus-minus
    # Goalies Only
    Regular_Games_Dressed: Optional[int] # games dressed
    Regular_GAA: Optional[float] # Goals against average
    Regular_Saves_Percentage: Optional[float] # Save percentage
    Regular_Goals_Against : Optional[int] # goals against
    Regular_Saves: Optional[int] # saves
    Regular_Shutouts: Optional[int] # shutouts
    Regular_WLT: Optional[str] # win-lose-tie
    Regular_TOI: Optional[str] # time on ice
    # Postseason
    Postseason_Games_Played: Optional[int] # games played
    # field players only
    Postseason_Goals: Optional[int] # goals
    Postseason_Assists: Optional[int] # assists
    Postseason_Total_Points: Optional[int] # points
    Postseason_Penalty_Minutes: Optional[int] # penalty minutes
    Postseason_Plus_Minus: Optional[int] # plus-minus
    # Goalies Only
    Postseason_Games_Dressed: Optional[int] # games dressed
    Postseason_GAA: Optional[float] # Goals against average
    Postseason_Saves_Percentage: Optional[float] # Save percentage
    Postseason_Goals_Against : Optional[int] # goals against
    Postseason_Saves: Optional[int] # saves
    Postseason_Shutouts: Optional[int] # shutouts
    Postseason_WLT: Optional[str] # win-lose-tie
    Postseason_TOI: Optional[str] # time on ice
# похоже, что проще всего сделать один класс со всеми полями - как рег, так и пост
    @classmethod
    def from_tag(cls, data, tag):
        # data = {'Player_name':player_name, 'Player_link': player_link}
        params = {
                'Season': 'season', 
                'Team':'team', 
                'League':'league',
                'Regular_Games_Played':'regular gp', 
                'Regular_Goals':'regular g', 
                'Regular_Assists':'regular a', 
                'Regular_Total_Points':'regular tp', 
                'Regular_Penalty_Minutes':'regular pim', 
                'Regular_Plus_Minus':'regular pm', 
                'Regular_Games_Dressed':'regular gd', 
                'Regular_GAA':'regular gaa', 
                'Regular_Saves_Percentage':'regular svp', 
                'Regular_Goals_Against':'regular ga', 
                'Regular_Saves':'regular svs', 
                'Regular_Shutouts':'regular so', 
                'Regular_WLT':'regular wlt', 
                'Regular_TOI':'regular toi', 
                'Postseason_Games_Played':'postseason gp', 
                'Postseason_Goals':'postseason g', 
                'Postseason_Assists':'postseason a', 
                'Postseason_Total_Points':'postseason tp', 
                'Postseason_Penalty_Minutes':'postseason pim', 
                'Postseason_Plus_Minus':'postseason pm', 
                'Postseason_Games_Dressed':'postseason gd', 
                'Postseason_GAA':'postseason gaa', 
                'Postseason_Saves_Percentage':'postseason svp', 
                'Postseason_Goals_Against':'postseason ga', 
                'Postseason_Saves':'postseason svs', 
                'Postseason_Shutouts':'postseason so', 
                'Postseason_WLT':'postseason wlt', 
                'Postseason_TOI':'postseason toi'}
                        
        for stats_param, tag_param in params.items():
            temp = tag.select_one(f'[class="{tag_param}"]')
            if temp:
                data[stats_param] = None if temp.text.strip() in ("-", "") else temp.text.strip().replace(' ', '')
            else:
                data[stats_param] = None
           
        return cls.parse_obj(data)



# regular
# https://www.eliteprospects.com/player/19555/sergei-belov?stats=postseason&sort=season
# postseason
# https://www.eliteprospects.com/player/19555/sergei-belov?stats=regular&sort=team
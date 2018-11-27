import plotly
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import iplot
from itertools import chain
import numpy as np
from tqdm import tqdm

def load_shooting_df():
    #Get Shot on and Against
    plays_df = pd.read_csv('data/game_plays.csv')
    shooting_df = plays_df.loc[plays_df.event.isin(['Goal','Shot']),:]

    #Format Shot by and Goalie
    shooting_df.loc[:,'shot_by'] = shooting_df['description']\
    .apply(lambda x: ' '.join(x.split()[0:2])).values
    shooting_df.loc[:,'goalie'] = shooting_df['description']\
    .apply(lambda x: ' '.join(x.split()[-2:])).values

    ## X and Y are inverted in the dataset vs our chart
    shooting_df.loc[:,'X'] = shooting_df['st_y'].apply(lambda x: x*500/85).values
    shooting_df.loc[:,'Y'] = shooting_df['st_x'].apply(lambda y: y*500/85).values

    shooting_df = shooting_df.loc[shooting_df['Y']>0,:] #ignore shots below center ice
    shooting_df = shooting_df.loc[shooting_df['Y']<516.5,:] #ignore shots below center ice
    return shooting_df


def load_expanded_shooting_df():
	shot_df = load_shooting_df()

	#Load Team Info
	team_info = pd.read_csv('data/team_info.csv')
	team_info['combined_name'] = team_info.shortName + ' ' + team_info.teamName
	team_info.drop(['franchiseId','shortName','teamName','abbreviation','link'],
	               axis = 1,inplace=True)

	#Load Games Dataset
	games_df = pd.read_csv('data/game.csv')
	games_df.drop(['venue_link','venue_time_zone_id'], axis= 1, inplace= True)

	#Load and Drop Unused Columns
	team_info = pd.read_csv('data/team_info.csv')
	team_info['combined_name'] = team_info.shortName + ' ' + team_info.teamName
	team_info.drop(['franchiseId','shortName','teamName','abbreviation','link'],
	               axis = 1,inplace=True)

	#Create home and away datasets for joining
	away_info = team_info.copy()
	away_info.columns = ['away_team_id','away_team_name']
	home_info = team_info.copy()
	home_info.columns = ['home_team_id','home_team_name']

	#Merge Columns
	games_df = games_df.merge(away_info)
	games_df = games_df.merge(home_info)
	shot_df = shot_df.merge(games_df,on='game_id')

	## Get unique games
	unique_games = shot_df.game_id.unique()
	print("Loaded {} Unique Games".format(len(unique_games)))
	return shot_df,unique_games

def load_rebounds_df():
    shot_df, unique_games = load_expanded_shooting_df()
    shot_df['shotTimeDiff'] = 0
    shot_df['nextShotResult'] = 'None'
    for gameid in tqdm(unique_games):
        game_shot_df = shot_df.loc[shot_df.game_id == gameid,:].sort_values('play_num')

        ## Set Home and Away Team
        away_df = game_shot_df.loc[game_shot_df.team_id_for == \
                                   game_shot_df.away_team_id,:]
        home_df = game_shot_df.loc[game_shot_df.team_id_for == \
                                   game_shot_df.home_team_id,:]

        ## Add shotTimeDiff column
        shot_df.loc[away_df.index.values,'shotTimeDiff'] = \
        -away_df['periodTime'] + away_df['periodTime'].shift(-1)
        shot_df.loc[home_df.index.values,'shotTimeDiff'] = \
        -home_df['periodTime'] + home_df['periodTime'].shift(-1)

        ## Add nextShotResult
        shot_df.loc[away_df.index.values,'nextShotResult'] = \
        away_df['event'].shift(-1).values
        shot_df.loc[home_df.index.values,'nextShotResult'] = \
        home_df['event'].shift(-1).values
    return shot_df
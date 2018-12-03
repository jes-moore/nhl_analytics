import plotly
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import iplot
from itertools import chain
import numpy as np
from tqdm import tqdm
import time

def load_shooting_df():
    #Get Shot on and Against
    plays_df = pd.read_csv('data/game_plays.csv')
    shooting_df = plays_df.loc[plays_df.event.isin(['Goal','Shot']),:]

    #Format Shot by and Goalie
    shooting_df = shooting_df.assign(shot_by = \
    	shooting_df['description'].apply(lambda x: ' '.join(x.split()[0:2])).values)

    shooting_df = shooting_df.assign(goalie = \
    	shooting_df['description'].apply(lambda x: ' '.join(x.split()[-2:])).values)

    ## X and Y are inverted in the dataset vs our chart
    shooting_df = shooting_df.assign(X =\
    	shooting_df['st_y'].apply(lambda x: x*500/85).values)
    shooting_df = shooting_df.assign(Y =\
    	shooting_df['st_x'].apply(lambda x: x*500/85).values)


    # shooting_df.loc[:,'shot_by'] = shooting_df['description']\
    # .apply(lambda x: ' '.join(x.split()[0:2])).values
    # shooting_df.loc[:,'goalie'] = shooting_df['description']\
    # .apply(lambda x: ' '.join(x.split()[-2:])).values

    ## X and Y are inverted in the dataset vs our chart
    # shooting_df.loc[:,'X'] = shooting_df['st_y'].apply(lambda x: x*500/85).values
    # shooting_df.loc[:,'Y'] = shooting_df['st_x'].apply(lambda y: y*500/85).values

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
	time.sleep(0.5) #For printing issue in notebooks
	return shot_df,unique_games

def load_rebounds_df():
    shot_df, unique_games = load_expanded_shooting_df()
    shot_df['shotTimeDiff'] = 0
    shot_df['nextShotResult'] = 'None'
    shot_df['nextShotX'] = 0
    shot_df['nextShotY'] = 0
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

        ## Add column on data from next shot
        shot_df.loc[away_df.index.values,'nextShotX'] = away_df['X'].shift(-1).values
        shot_df.loc[home_df.index.values,'nextShotY'] = home_df['Y'].shift(-1).values
    return shot_df

def get_seasonal_summary(game_type = 'R'):
    seasonal_df = pd.read_csv('data/game_teams_stats.csv')
    seasonal_df['season'] = seasonal_df['game_id'].apply(lambda x: str(x)[0:4])

    ## Load team info
    team_info = pd.read_csv('data/team_info.csv')
    team_info['combined_name'] = team_info.shortName + ' ' + team_info.teamName
    team_info.drop(['franchiseId','shortName','teamName','abbreviation','link'],
                   axis = 1,inplace=True)

    ## Load playoff/reg season
    type_df = pd.read_csv('data/game.csv')[['game_id','type']]

    ## Merge DF's and Count wins/losses
    seasonal_df = seasonal_df.merge(team_info)
    seasonal_df = seasonal_df.merge(type_df)
    seasonal_df['win'] = seasonal_df.won == True
    seasonal_df['loss'] = seasonal_df.won == False

    seasonal_df = seasonal_df.groupby(['season','combined_name','type']).agg('sum').reset_index()
    seasonal_df.drop(['game_id','team_id','won'],inplace=True, axis=1)
    seasonal_df = seasonal_df[seasonal_df.season != '2012']

    ## Analyse game type
    if game_type == 'R':
        seasonal_df = seasonal_df[seasonal_df.type == 'R']
    elif game_type == 'P':
        seasonal_df = seasonal_df[seasonal_df.type == 'R']
    else:
        print("Failed type")
        return
    return seasonal_df
## Credit to https://moderndata.plot.ly/nhl-shots-analysis-using-plotly-shapes/
import plotly
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import iplot
from itertools import chain
import numpy as np


def load_shooting_df():
    #Get Shot on and Against
    plays_df = pd.read_csv('data/game_plays.csv')
    shooting_df = plays_df[plays_df.event.isin(['Goal','Shot'])]

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

def create_shotbox_df():
    shooting_df = load_shooting_df()
    ## Convert dots to boxes that are 25 x 25.825
    x0 = [num for num in range(-250,250,25)] * 20
    x1 = [num for num in range(-225,275,25)] * 20
    y0 = list(chain.from_iterable([[num]*20 for num in range(0,516500,25825)]))
    y1 = list(chain.from_iterable([[num]*20 for num in range(25825,542325,25825)]))

    shot_boxes = pd.DataFrame({'x0':x0,
                               'x1':x1,
                               'y0':y0,
                               'y1':y1
                              })
    ## Set box size to proper dimension
    shot_boxes['y0'] = shot_boxes['y0'].values/1000
    shot_boxes['y1'] = shot_boxes['y1'].values/1000

    ## Get num shots and num goals by box
    num_shots = []
    num_goals = []
    for ix,box in shot_boxes.iterrows():
        box_df = shooting_df[(shooting_df.X >= box['x0']) & 
                             (shooting_df.X < box['x1']) &
                             (shooting_df.Y >= box['y0']) & 
                             (shooting_df.Y < box['y1'])
                            ]
        num_shots.append(box_df.agg({'event':'count'}).values[0])
        num_goals.append(box_df[box_df.event == 'Goal'].agg({'event':'count'}).values[0])

    shot_boxes['num_shots'] = num_shots
    shot_boxes['num_goals'] = num_goals
    shot_boxes['goal_ratio'] = shot_boxes['num_goals']/ shot_boxes['num_shots']

    shot_boxes = shot_boxes[shot_boxes.num_goals > 10]
    shot_boxes = shot_boxes[shot_boxes.num_shots > 50]

    ## Scale for Plotting
    shot_boxes['goal_ratio_colour'] = \
    shot_boxes['goal_ratio'] / (1 * shot_boxes['goal_ratio'].max())

    shot_boxes['num_shot_colour'] = \
    shot_boxes['num_shots'] / (1 * shot_boxes['num_shots'].max())

    shot_boxes['num_goal_colour'] = \
    np.log2(shot_boxes['num_goals']) / (1 * shot_boxes['num_goals'].max())

    ## Format for Plotting Hovering Data
    shot_boxes['centroid_x'] = shot_boxes['x1'] - ((shot_boxes['x1'] - shot_boxes['x0'])/2)
    shot_boxes['centroid_y'] = shot_boxes['y1'] - ((shot_boxes['y1'] - shot_boxes['y0'])/2)

    shot_boxes['goal_ratio_text'] = \
    'Scoring Ratio = ' + shot_boxes['goal_ratio'].apply(lambda x:"{0:.2f}%".format(x * 100))\
    + ' <br>Number of Shots = ' + shot_boxes['num_shots'].apply(lambda x: str(x))\
    + ' <br>Number of Goals = ' + shot_boxes['num_goals'].apply(lambda x: str(x))
    return shot_boxes

def create_shotbox_shape(shot_boxes):
    ## Convert boxes into plottable shape
    shot_box_shapes = []
    for ix,box in shot_boxes.iterrows():
        shot_box_shapes.append(
            dict(
                type='rect',
                xref='x',
                yref='y',
                x0=box['x0'],
                y0=box['y0'],
                x1=box['x1'],
                y1=box['y1'],
                line=dict(width=0),
                fillcolor='rgba(255, 0, 0,' + str(box['num_shot_colour']) + ')' 
            )
        )
    return shot_box_shapes


def rink_shapes():    
    outer_rect_shape = dict(
                type='rect',
                xref='x',
                yref='y',
                x0='-250',
                y0='0',
                x1='250',
                y1='516.2',
                line=dict(
                    width=1,
                )
    )


    outer_line_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='200',
                y0='580',
                x1='-200',
                y1='580',
                line=dict(
                    width=1,
                )
    )



    outer_arc1_shape = dict(
                type='path',
                xref='x',
                yref='y',
                path='M 200 580 C 217 574, 247 532, 250 516.2',
                line=dict(
                    width=1,
                )
    )


    outer_arc2_shape = dict(
                type='path',
                xref='x',
                yref='y',
                path='M -200 580 C -217 574, -247 532, -250 516.2',
                line=dict(
                    width=1,
                )
    )

    center_red_line_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-250',
                y0='0',
                x1='250',
                y1='0',
                line=dict(
                    width=1,
                    color='rgba(255, 0, 0, 1)'
                )
    )

    end_line_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-250',
                y0='516.2',
                x1='250',
                y1='516.2',
                line=dict(
                    width=1,
                    color='rgba(255, 0, 0, 1)'
                )
    )

    blue_line_shape = dict(
                type='rect',
                xref='x',
                yref='y',
                x0='250',
                y0='150.8',
                x1='-250',
                y1='145',
                line=dict(
                    color='rgba(0, 0, 255, 1)',
                    width=1
                ),
                fillcolor='rgba(0, 0, 255, 1)'
    )

    center_blue_spot_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='2.94',
                y0='2.8',
                x1='-2.94',
                y1='-2.8',
                line=dict(
                    color='rgba(0, 0, 255, 1)',
                    width=1
                ),
                fillcolor='rgba(0, 0, 255, 1)'
    )

    red_spot1_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='135.5',
                y0='121.8',
                x1='123.5',
                y1='110.2',
                line=dict(
                    color='rgba(255, 0, 0, 1)',
                    width=1
                ),
                fillcolor='rgba(255, 0, 0, 1)'
    )

    red_spot2_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='-135.5',
                y0='121.8',
                x1='-123.5',
                y1='110.2',
                line=dict(
                    color='rgba(255, 0, 0, 1)',
                    width=1
                ),
                fillcolor='rgba(255, 0, 0, 1)'
    )

    red_spot3_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='135.5',
                y0='406',
                x1='123.5',
                y1='394',
                line=dict(
                    color='rgba(255, 0, 0, 1)',
                    width=1
                ),
                fillcolor='rgba(255, 0, 0, 1)'
    )

    red_spot4_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='-135.5',
                y0='406',
                x1='-123.5',
                y1='394',
                line=dict(
                    color='rgba(255, 0, 0, 1)',
                    width=1
                ),
                fillcolor='rgba(255, 0, 0, 1)'
    )

    red_spot1_circle_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='217.6',
                y0='487.2',
                x1='41.2',
                y1='313.2',
                line=dict(
                    width=1,
                    color='rgba(255, 0, 0, 1)'
                )
    )

    red_spot2_circle_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='-217.6',
                y0='487.2',
                x1='-41.2',
                y1='313.2',
                line=dict(
                    width=1,
                    color='rgba(255, 0, 0, 1)'
                )
    )

    center_ice_circle_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='88.2',
                y0='88.2',
                x1='-88.2',
                y1='-88.2',
                line=dict(
                    width=1,
                    color='rgba(0, 0, 255, 1)'
                )
    )

    parallel_line1_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='230',
                y0='416.4',
                x1='217.8',
                y1='416.4',
                line=dict(
                    color='rgba(255, 0, 0, 1)',
                    width=1
                )
    )

    parallel_line2_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='230',
                y0='384',
                x1='217.8',
                y1='384',
                line=dict(
                    color='rgba(255, 0, 0, 1)',
                    width=1
                )
    )

    parallel_line3_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-230',
                y0='416.4',
                x1='-217.8',
                y1='416.4',
                line=dict(
                    color='rgba(255, 0, 0, 1)',
                    width=1
                )
    )

    parallel_line4_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-230',
                y0='384',
                x1='-217.8',
                y1='384',
                line=dict(
                    color='rgba(255, 0, 0, 1)',
                    width=1
                )
    )

    faceoff_line1_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='141.17',
                y0='423.4',
                x1='141.17',
                y1='377',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )

    faceoff_line2_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='117.62',
                y0='423.4',
                x1='117.62',
                y1='377',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )

    faceoff_line3_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='153',
                y0='406',
                x1='105.8',
                y1='406',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )

    faceoff_line4_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='153',
                y0='394.4',
                x1='105.8',
                y1='394.4',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )

    faceoff_line5_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-141.17',
                y0='423.4',
                x1='-141.17',
                y1='377',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )

    faceoff_line6_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-117.62',
                y0='423.4',
                x1='-117.62',
                y1='377',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )

    faceoff_line7_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-153',
                y0='406',
                x1='-105.8',
                y1='406',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )

    faceoff_line8_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-153',
                y0='394.4',
                x1='-105.8',
                y1='394.4',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )

    goal_line1_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='64.7',
                y0='516.2',
                x1='82.3',
                y1='580',
                line=dict(
                    width=1
                )
    )

    goal_line2_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='23.5',
                y0='516.2',
                x1='23.5',
                y1='493',
                line=dict(
                    width=1
                )
    )

    goal_line3_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-64.7',
                y0='516.2',
                x1='-82.3',
                y1='580',
                line=dict(
                    width=1
                )
    )

    goal_line4_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-23.5',
                y0='516.2',
                x1='-23.5',
                y1='493',
                line=dict(
                    width=1
                )
    )

    # mirror images of "goal_line1" and "goal_line2" along with the Y-axis

    goal_arc1_shape = dict(
                type='path',
                xref='x',
                yref='y',
                path='M 23.5 493 C 20 480, -20 480, -23.5 493',
                line=dict(
                    width=1,
                )
    )

    goal_arc2_shape = dict(
                type='path',
                xref='x',
                yref='y',
                path='M 17.6 516.2 C 15 530, -15 530, -17.6 516.2',
                line=dict(
                    width=1,
                )
    )

    referee_crease_shape = dict(
                type='path',
                xref='x',
                yref='y',
                path='M ',
                line=dict(
                    width=1,
                    color='rgba(255, 0, 0, 1)'
                )
    )


    rink_shapes = []
    #Main Rink Shape
    rink_shapes.append(outer_rect_shape)
    rink_shapes.append(outer_line_shape)
    rink_shapes.append(outer_arc1_shape)
    rink_shapes.append(outer_arc2_shape)

    #Main Lines Shapes
    rink_shapes.append(center_red_line_shape)
    rink_shapes.append(end_line_shape)
    rink_shapes.append(blue_line_shape)

    #Faceoff Dots
    rink_shapes.append(center_blue_spot_shape)
    rink_shapes.append(red_spot1_shape)
    rink_shapes.append(red_spot2_shape)
    rink_shapes.append(red_spot3_shape)
    rink_shapes.append(red_spot4_shape)

    #Faceoff Circles
    rink_shapes.append(red_spot1_circle_shape)
    rink_shapes.append(red_spot2_circle_shape)
    rink_shapes.append(center_ice_circle_shape)
    #Faceoff Lines
    rink_shapes.append(parallel_line1_shape)
    rink_shapes.append(parallel_line2_shape)
    rink_shapes.append(faceoff_line1_shape)
    rink_shapes.append(faceoff_line2_shape)
    rink_shapes.append(faceoff_line3_shape)
    rink_shapes.append(faceoff_line4_shape)
    #Other Side
    rink_shapes.append(parallel_line3_shape)
    rink_shapes.append(parallel_line4_shape)
    rink_shapes.append(faceoff_line5_shape)
    rink_shapes.append(faceoff_line6_shape)
    rink_shapes.append(faceoff_line7_shape)
    rink_shapes.append(faceoff_line8_shape)


    #Goalie Shapes
    rink_shapes.append(goal_line1_shape)
    rink_shapes.append(goal_line2_shape)
    rink_shapes.append(goal_line3_shape)
    rink_shapes.append(goal_line4_shape)

    rink_shapes.append(goal_arc1_shape)
    rink_shapes.append(goal_arc2_shape)
    rink_shapes.append(referee_crease_shape)
    return rink_shapes
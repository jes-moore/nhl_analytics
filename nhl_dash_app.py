## Plotting Libraries
from plotting import *

## Dashboard Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

## App Data
shooting_df = load_shooting_df()
shot_boxes = create_shotbox_df(shooting_df)

## Main App Layout and Graphing
app.layout = html.Div([
    # html.H1('NHL Analytics'),
    html.Div([
        html.Div([
            # html.H3('Column 1'),
            dcc.Graph(
                id='eg1',
                figure=plot_goal_ratio(shot_boxes),
                config={"displaylogo": False}
                )], className="six columns"),
        html.Div([
            # html.H3('Column 2'),
            dcc.Graph(
                id='eg2',
                figure=plot_goal_ratio(shot_boxes),
                config={"displaylogo": False}
                )], className="six columns"),
        ], className="row"),
    html.Div(id='container')
    ])

## Callbacks

# @app.callback(
#     Output('eg1', 'figure'),
#     [],
#     [   
#         State('eg1', 'figure'),
#         State('eg1', 'hoverData'),
#     ],
#     [
#         Event('eg1', 'hover')
#     ]
# )
# def update_graph(eg1, data):

#     if data is not None:
#         # get the information about the hover point
#         hover_curve_idx = data['points'][0]['curveNumber']
#         hover_pt_idx = data['points'][0]['pointIndex']
#         data_to_highlight = eg1['data'][hover_curve_idx]

#         # change the last curve which is reserved for highlight
#         eg1['data'][-1]['x'] = [data_to_highlight['x'][hover_pt_idx]]
#         eg1['data'][-1]['y'] = [data_to_highlight['y'][hover_pt_idx]]

#     return eg1



if __name__ == '__main__':
    app.run_server(debug=True)
## Plotting Libraries
from plotting import *

## Dashboard Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

## App Data
shooting_df = load_shooting_df()
shot_boxes = create_shotbox_df(shooting_df)

app.layout = html.Div(children=[
    html.H1(children='NHL Analytics'),
    html.Div(children=''''''),
    html.Div([
        html.Div([
            html.H3('Column 1'),
            dcc.Graph(
                id='eg1',
                figure=plot_goal_ratio(shot_boxes),
                config={"displaylogo": False}
                )
            ], 
            className="six columns"),
        html.Div([
            html.H3('Column 2'),
            dcc.Graph(
                id='eg2',
                figure=plot_goal_ratio(shot_boxes),
                config={"displaylogo": False}
                )
            ], className="six columns"),
        ], className="row")
    ])

if __name__ == '__main__':
    app.run_server(debug=False)
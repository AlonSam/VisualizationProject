import dash
from dash import dcc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output
import pandas as pd

from components import get_team_dropdown_options, get_stage_options, get_slider_marks
from consts import LABEL_TO_DESC
from figures import *
from utils import preprocess_matches_df, preprocess_forecasts_df

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

load_figure_template('FLATLY')

forecasts_df = preprocess_forecasts_df(
    pd.read_csv('https://raw.githubusercontent.com/AlonSam/VisualizationProject/main/wc_forecasts.csv'))
matches_df = preprocess_matches_df(
    pd.read_csv('https://raw.githubusercontent.com/AlonSam/VisualizationProject/main/wc_matches.csv'))

win_probability_fig = get_win_probability_fig(forecasts_df, ['Brazil', 'France'])
top_teams_fig = get_top_teams_fig(forecasts_df, 'Win World Cup')
goals_vs_projected_fig = get_goals_vs_projected_fig(matches_df, 0)
match_probability_fig = get_match_probability_fig(matches_df, 0)
chances_saudi_arabia_fig = get_chances_saudi_arabia_fig(forecasts_df)


def get_dash_layout():
    layout = dbc.Container(
        [
            html.H1(children="Argentina\'s Road to the Cup", className='mt-4 mb-4', style={'text-align': 'center'}),
            dbc.Row(
                [
                    dbc.Col(get_argentina_matches_won_card(matches_df), width={'size': 2, 'offset': 2, 'order': 1}),
                    dbc.Col(get_argentina_goals_card(matches_df), width={'size': 2, 'offset': 0, 'order': 2}),
                    dbc.Col(get_argentina_goals_conceded_card(matches_df), width={'size': 2, 'offset': 0, 'order': 3}),
                    dbc.Col(get_one_world_cup_card(), width={'size': 2, 'offset': 0, 'order': 4})

                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(id='first-row-first-col',
                                     children=[
                                         html.Label('Select team:',
                                                    style={'font-weight': 'bold', 'text-align': 'center'}),
                                         dcc.Dropdown(
                                             id='team-dropdown',
                                             options=get_team_dropdown_options(forecasts_df),
                                             value=['Brazil', 'France'],
                                             multi=True,
                                         ),
                                         dcc.Graph(
                                             id='win-probability-graph',
                                             figure=win_probability_fig,
                                         )
                                     ])
                        ],
                        width={'size': 4, 'offset': 2, 'order': 1},
                    ),
                    dbc.Col(
                        [
                            html.Div(id='first-row-second-col',
                                     children=[
                                         html.Label('Select round:',
                                                    style={'font-weight': 'bold', 'text-align': 'center'}),
                                         dcc.Dropdown(
                                             id='round-dropdown',
                                             options=get_stage_options(),
                                             value='Win World Cup'
                                         ),
                                         dcc.Graph(
                                             id='top-teams-graph',
                                             figure=top_teams_fig,
                                         )
                                     ]
                                     )
                        ],
                        width={'size': 4, 'offset': 0, 'order': 2},
                    )
                ],
                className='mt-4 mb-4'
            ),

            dbc.Row(
                [
                    dbc.Row(
                        [
                            dbc.Col([
                                html.Label('Select Match:', style={'font-weight': 'bold', 'text-align': 'center',
                                                                   'justify-content': 'center', 'display': 'flex'}),
                                html.Div(id='team-match-slider-container', children=[
                                    dcc.Slider(0, 6, id='team-match-slider', step=1,
                                               marks=get_slider_marks(matches_df, 'Argentina'), value=0)
                                ],
                                         style={'height': '100px'}),
                            ],
                                width={'size': 8, 'offset': 2, 'order': 1},
                            )
                        ]),
                    dbc.Row(
                        [
                            dbc.Col([
                                dcc.Graph(
                                    id='goals-vs-projected-graph',
                                    figure=goals_vs_projected_fig,
                                    clear_on_unhover=True
                                ),
                                dcc.Tooltip(id='graph-tooltip')
                            ],
                                width={'size': 4, 'offset': 2, 'order': 1},
                            ),
                            dbc.Col([
                                dcc.Graph(
                                    id='match-probabilities-graph',
                                    figure=match_probability_fig,
                                )
                            ],
                                width={'size': 4, 'offset': 0, 'order': 2},
                            )
                        ]),
                ],
                className='mt-4 mb-4'

            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(
                                id='before-and-after-saudi-arabia',
                                figure=chances_saudi_arabia_fig,
                            )
                        ],
                        width={'size': 8, 'offset': 2, 'order': 1},
                    )
                ],
                className='mt-4 mb-4'
            )
        ],
        fluid=True
    )

    return layout


@app.callback(
    Output(component_id='win-probability-graph', component_property='figure'),
    [Input(component_id='team-dropdown', component_property='value')]
)
def build_win_probability_fig(teams):
    return get_win_probability_fig(forecasts_df, teams)


@app.callback(
    Output(component_id='top-teams-graph', component_property='figure'),
    [Input(component_id='round-dropdown', component_property='value')]
)
def build_top_teams_fig(stage):
    return get_top_teams_fig(forecasts_df, stage)


@app.callback(
    Output(component_id='goals-vs-projected-graph', component_property='figure'),
    [Input(component_id='team-match-slider', component_property='value')]
)
def build_goals_vs_projected_fig(match_num):
    return get_goals_vs_projected_fig(matches_df, match_num)


@app.callback(
    Output(component_id='graph-tooltip', component_property='show'),
    Output(component_id='graph-tooltip', component_property='bbox'),
    Output(component_id='graph-tooltip', component_property='children'),
    Input(component_id='goals-vs-projected-graph', component_property='hoverData'),
)
def display_hover(hoverData):
    if hoverData is None:
        return False, None, ''
    pt = hoverData['points'][0]
    bbox = pt['bbox']
    label = pt['label']
    desc = LABEL_TO_DESC[label]
    children = [
        html.Div([
            html.H3(f'{label}', style={'text-align': 'center', 'color': 'darkblue', 'overflow-wrap': 'break-word'}),
            html.P(f'{desc}')
            ], style={'width': '200px', 'white-space': 'normal'}
        )
        ]
    return True, bbox, children


@app.callback(
    Output(component_id='match-probabilities-graph', component_property='figure'),
    [Input(component_id='team-match-slider', component_property='value')]
)
def build_match_probability_fig(match_num):
    return get_match_probability_fig(matches_df, match_num)


app.layout = get_dash_layout()

if __name__ == '__main__':
    app.run_server(debug=True)

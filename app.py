import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output
import pandas as pd

from components import get_team_dropdown_options, get_stage_options, get_team_match_options
from figures import *
from utils import preprocess_matches_df, preprocess_forecasts_df

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

load_figure_template('FLATLY')

forecasts_df = preprocess_forecasts_df(pd.read_csv('wc_forecasts.csv'))
matches_df = preprocess_matches_df(pd.read_csv('wc_matches.csv'))

win_probability_fig = get_win_probability_fig(forecasts_df, ['Brazil', 'France'])
top_teams_fig = get_top_teams_fig(forecasts_df, 'Win League')
goals_vs_projected_fig = get_goals_vs_projected_fig(matches_df, 'Saudi Arabia')
match_probability_fig = get_match_probability_fig(matches_df, 'Saudi Arabia')
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
                                             value='Win League'
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
                                html.Label('Select opponent:', style={'font-weight': 'bold', 'text-align': 'center'}),
                                dcc.Dropdown(
                                    id='team-match-dropdown',
                                    options=get_team_match_options(matches_df, 'Argentina'),
                                    value='Saudi Arabia',
                                )
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
                                ),
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
    [Input(component_id='team-match-dropdown', component_property='value')]
)
def build_goals_vs_projected_fig(opponent):
    return get_goals_vs_projected_fig(matches_df, opponent)


@app.callback(
    Output(component_id='match-probabilities-graph', component_property='figure'),
    [Input(component_id='team-match-dropdown', component_property='value')]
)
def build_match_probability_fig(opponent):
    return get_match_probability_fig(matches_df, opponent)


app.layout = get_dash_layout()

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)

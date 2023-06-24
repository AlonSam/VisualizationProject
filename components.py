from consts import STAGE_PROBABILITIES_COLUMNS, MATCH_TO_ROUND_MAP
from utils import get_team_matches


def get_team_dropdown_options(df):
    teams = df['team'].unique()
    return [{'label': team, 'value': team} for team in sorted(teams) if team != 'Argentina']


def get_stage_options():
    stages = [" ".join([word.capitalize() for word in stage.split('_')]) for stage in STAGE_PROBABILITIES_COLUMNS]
    stages = [stage.replace('League', 'World Cup') for stage in stages]
    return [{'label': stage, 'value': stage} for stage in stages]


def get_team_match_options(df, team):
    matches_df = get_team_matches(df, team)
    options = []
    for i, match in matches_df.iterrows():
        if match['team1'] == team:
            opponent = match['team2']
        else:
            opponent = match['team1']
        options.append({'label': f'vs {opponent}', 'value': opponent})
    return options


def get_slider_marks(df, team):
    matches_df = get_team_matches(df, team)
    marks = {}
    match_num = 0
    for _, match in matches_df.iterrows():
        if match['team1'] == team:
            opponent = match['team2']
        else:
            opponent = match['team1']
        marks[match_num] = {'label': f'{MATCH_TO_ROUND_MAP[match_num]} vs {opponent}',
                            'style': {'text-align': 'left',
                                      'font-size': '14px',
                                      'color': 'black'}
                            }
        match_num += 1
    return marks

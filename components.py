from consts import STAGE_PROBABILITIES_COLUMNS
from utils import get_team_matches


def get_team_dropdown_options(df):
    teams = df['team'].unique()
    return [{'label': team, 'value': team} for team in teams if team != 'Argentina']


def get_stage_options():
    stages = [" ".join([word.capitalize() for word in stage.split('_')]) for stage in STAGE_PROBABILITIES_COLUMNS]
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

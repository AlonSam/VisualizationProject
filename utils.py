from datetime import datetime

import pandas as pd

from consts import DATE_TO_ROUND_MAP


def preprocess_forecasts_df(df):
    df['date'] = df['forecast_timestamp'].apply(
        lambda x: datetime.strptime(x[:10], '%Y-%m-%d').date())
    df.sort_values(by='date', inplace=True)
    df['match'] = [i for i in range(1, len(df) + 1)]
    df['round'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df['round'] = df['round'].apply(lambda x: DATE_TO_ROUND_MAP[x])
    return df


def preprocess_matches_df(df):
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df.sort_values(by='date', inplace=True)
    df['match'] = [i for i in range(1, len(df) + 1)]
    return df


def get_first_round(df):
    min_date = df['date'].min()
    return df[df['date'] == min_date]


def get_team_forecasts(forecasts_df, team):
    return forecasts_df[forecasts_df['team'] == team]


def get_team_matches(matches_df, team):
    return matches_df[(matches_df['team1'] == team) | (matches_df['team2'] == team)]


def get_match(matches_df, team1, team2):
    return matches_df[(matches_df['team1'] == team1) & (matches_df['team2'] == team2) | (matches_df['team1'] == team2) & (matches_df['team2'] == team1)]
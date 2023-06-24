import plotly.graph_objs as go
from dash import html
import dash_bootstrap_components as dbc

from consts import team_color_mapping, STAGE_PROBABILITIES_COLUMNS, ARGENTINA, METRICS_TO_NAME
from utils import get_first_round, get_match, get_team_matches


def get_win_probability_fig(forecasts_df, teams):
    forecasts_df = forecasts_df[forecasts_df['round'] != 'After final']
    teams_df = forecasts_df[forecasts_df['team'].isin(teams)]
    argentina_df = forecasts_df[forecasts_df['team'] == ARGENTINA]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=argentina_df['round'], y=argentina_df['win_league'], mode='lines+markers',
                             line=dict(color=team_color_mapping[ARGENTINA], width=3),
                             marker=dict(color=team_color_mapping[ARGENTINA], size=12),
                             name=ARGENTINA))
    for team, group in teams_df.groupby('team'):
        fig.add_trace(go.Scatter(x=group['round'], y=group['win_league'], mode='lines+markers', opacity=0.4,
                                 marker_color=team_color_mapping[team], name=team, marker_size=12,
                                 marker_opacity=0.5, line=dict(color=team_color_mapping[team], width=3)))
    fig.update_traces(hovertemplate='<b>%{x}</b><br>%{y:.0%}')
    fig.update_layout(xaxis_title='Round', title='Probability to Win World Cup by Round', title_x=0.5,
                      yaxis=dict(tickformat=".0%", title='Probability to Win World Cup', title_font_size=16),
                      xaxis_title_font_size=16)
    return fig


def get_top_teams_fig(forecasts_df, stage):
    stage_label = stage.replace('World Cup', 'League')
    stage_column = "_".join(word.lower() for word in stage_label.split(' '))
    first_round_df = get_first_round(forecasts_df)
    first_round_df.sort_values(by=stage_column, inplace=True, ascending=False)
    top_start_df = first_round_df.iloc[:10, :]
    top_start_df['colors'] = top_start_df['team'].apply(
        lambda x: 'lightgrey' if x != 'Argentina' else team_color_mapping[x])
    fig = go.Figure(
        data=[go.Bar(x=top_start_df['team'], y=top_start_df[stage_column], marker_color=top_start_df['colors'],
                     hovertemplate='<b>%{x}</b><br>%{y:.0%}', text=top_start_df[stage_column].apply(
                lambda x: f'{x:.0%}'), textposition='inside', texttemplate='%{text}',
                     marker=dict(line=dict(color='black', width=1)))])
    fig.update_layout(title=f'Top National Teams by Probability to {stage}', xaxis_title='National Team',
                      yaxis=dict(tickformat=".0%", title=f'Probability to {stage}', title_font_size=16),
                      xaxis_title_font_size=16,
                      title_x=0.5)
    return fig


def get_goals_vs_projected_fig(matches_df, match_num):
    matches_df = get_team_matches(matches_df, ARGENTINA)
    opponent = matches_df.iloc[match_num]['team2'] if matches_df.iloc[match_num]['team1'] == ARGENTINA else \
        matches_df.iloc[match_num]['team1']
    match_df = get_match(matches_df, ARGENTINA, opponent)
    home_team, away_team = match_df['team1'].values[0], match_df['team2'].values[0]
    if home_team == ARGENTINA:
        argentina_df = match_df[[f'{metric}1' for metric in METRICS_TO_NAME.keys()]].iloc[0]
        opponent_df = match_df[[f'{metric}2' for metric in METRICS_TO_NAME.keys()]].iloc[0]
    else:
        argentina_df = match_df[[f'{metric}2' for metric in METRICS_TO_NAME.keys()]].iloc[0]
        opponent_df = match_df[[f'{metric}1' for metric in METRICS_TO_NAME.keys()]].iloc[0]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(METRICS_TO_NAME.values()), y=argentina_df, name=ARGENTINA, marker_color=team_color_mapping[ARGENTINA],
                         text=argentina_df, textposition='auto', textfont=dict(color='black', size=16),
                         texttemplate='%{y:.1f}',
                         marker=dict(line=dict(color='black', width=1))))
    fig.add_trace(go.Bar(x=list(METRICS_TO_NAME.values()), y=opponent_df, name=opponent, marker_color=team_color_mapping[opponent],
                         text=opponent_df, textposition='auto', textfont=dict(size=16),
                         texttemplate='%{y:.1f}',
                         marker=dict(line=dict(color='black', width=1))))
    fig.update_traces(hoverinfo='none', hovertemplate=None)
    fig.update_layout(title=f'Match Statistics',
                      xaxis_title='Metric',
                      yaxis=dict(title='Goals', titlefont_size=16),
                      xaxis=dict(titlefont_size=16),
                      title_x=0.5)
    return fig


def get_match_probability_fig(matches_df, match_num):
    matches_df = get_team_matches(matches_df, ARGENTINA)
    opponent = matches_df.iloc[match_num]['team2'] if matches_df.iloc[match_num]['team1'] == ARGENTINA else \
        matches_df.iloc[match_num]['team1']
    match_df = get_match(matches_df, ARGENTINA, opponent).iloc[0]
    fig = go.Figure()
    home_team = match_df['team1']
    away_team = match_df['team2']
    if match_df['probtie'] == 0:
        pull = [0, 0]
        prob_values = [match_df['prob1'], match_df['prob2']]
        labels = [f'{home_team} Win', f'{away_team} Win']
        colors = [team_color_mapping[home_team], team_color_mapping[away_team]]
    else:
        pull = [0.2, 0, 0] if home_team == ARGENTINA else [0, 0, 0.2]
        prob_values = [match_df['prob1'], match_df['probtie'], match_df['prob2']]
        labels = [f'{home_team} Win', 'Tie', f'{away_team} Win']
        colors = [team_color_mapping[home_team], 'lightgrey', team_color_mapping[away_team]]
    fig.add_trace(go.Pie(values=prob_values,
                         labels=labels,
                         hole=.3,
                         pull=pull))
    fig.update_traces(textinfo='value', textfont_size=20, hovertemplate='<b>%{label}</b><br> %{percent:.1%}',
                      marker=dict(colors=colors, line=dict(color='#000000', width=2)), texttemplate='%{percent:.1%}')
    fig.update_layout(title=f'Pre-Match Probabilities', yaxis=dict(tickformat=".0%", title_font_size=16),
                      title_x=0.5)
    return fig


def get_chances_saudi_arabia_fig(forecasts_df):
    argentina_df = forecasts_df[forecasts_df['team'] == ARGENTINA]
    chances_before = argentina_df.iloc[0, :][STAGE_PROBABILITIES_COLUMNS]
    chances_after = argentina_df.iloc[1, :][STAGE_PROBABILITIES_COLUMNS]
    stages = [" ".join([word.capitalize() for word in stage.split('_')]) for stage in STAGE_PROBABILITIES_COLUMNS]
    stages = [stage.replace('League', 'World Cup') for stage in stages]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=stages, y=chances_before, name='Before', marker_color=team_color_mapping[ARGENTINA],
                         text=chances_before, textposition='auto', textfont=dict(color='black', size=16),
                         texttemplate='%{text:.0%}',
                         marker=dict(line=dict(color='black', width=1))))
    fig.add_trace(go.Bar(x=stages, y=chances_after, name='After', marker_color='lightgrey',
                         text=chances_after, textposition='auto', textfont=dict(color='black', size=16),
                         texttemplate='%{text:.0%}',
                         marker=dict(line=dict(color='black', width=1))))
    fig.update_traces(hovertemplate='<b>%{x}</b><br> %{text:.0%}')
    fig.update_layout(title=f'{ARGENTINA} Probabilities to Reach Each Round Before and After Saudi Arabia Match',
                      xaxis_title='Stage',
                      yaxis=dict(tickformat=".0%", title='Probability to Reach Round', title_font=dict(size=16)),
                      xaxis=dict(title_font=dict(size=16)),
                      title_x=0.5)
    return fig


def get_argentina_matches_won_card(matches_df):
    argentina_matches = get_team_matches(matches_df, ARGENTINA)
    argentina_matches['won'] = argentina_matches.apply(
        lambda x: 1 if x['team1'] == ARGENTINA and x['score1'] >= x['score2'] else 1 if x['team2'] == ARGENTINA and x[
            'score2'] >= x['score1'] else 0, axis=1)
    total_matches_won = argentina_matches['won'].sum()
    card_content = [
        dbc.CardImg(
            src='https://e00-marca.uecdn.es/assets/multimedia/imagenes/2022/12/09/16706123218717.jpg',
            top=True,
            style={'opacity': '0.3'}
        ),
        dbc.CardImgOverlay(
            dbc.CardBody([
                html.H4("Matches Won", className="text-center", style={'font-size': '2rem'}),
                html.P(f'{total_matches_won}', className="text-center", style={'font-size': '3rem'}),
            ],
                style={'align-items': 'center', 'justify-content': 'center'}),
        )
    ]
    return dbc.Card(card_content, color="primary", outline=True, style={'height': '100%'})


def get_argentina_goals_card(matches_df):
    argentina_matches = get_team_matches(matches_df, ARGENTINA)
    argentina_matches['goals'] = argentina_matches.apply(
        lambda x: x['score1'] if x['team1'] == ARGENTINA else x['score2'], axis=1)
    total_goals = argentina_matches['goals'].sum()
    card_content = [
        dbc.CardImg(
            src='https://cdn.britannica.com/35/238335-050-2CB2EB8A/Lionel-Messi-Argentina-Netherlands-World-Cup-Qatar-2022.jpg',
            top=True,
            style={'opacity': '0.3'}
        ),
        dbc.CardImgOverlay(
            dbc.CardBody([
                html.H4("Goals Scored", className="text-center", style={'font-size': '2rem'}),
                html.P(f'{total_goals}', className="text-center", style={'font-size': '3rem'}),
            ]),
        )
    ]
    return dbc.Card(card_content, color="primary", outline=True, style={'height': '100%'})


def get_argentina_goals_conceded_card(matches_df):
    argentina_matches = get_team_matches(matches_df, ARGENTINA)
    argentina_matches['goals'] = argentina_matches.apply(
        lambda x: x['score1'] if x['team1'] != ARGENTINA else x['score2'], axis=1)
    total_goals = argentina_matches['goals'].sum()
    card_content = [
        dbc.CardImg(
            src='https://static.independent.co.uk/2022/12/19/08/urnpublicidap.org8c457abf90544877a4818c25ceaca677.jpg',
            top=True,
            style={'opacity': '0.3'}
        ),
        dbc.CardImgOverlay(
            dbc.CardBody([
                html.H4("Goals Conceded", className="text-center", style={'font-size': '1.9rem'}),
                html.P(f'{total_goals}', className="text-center", style={'font-size': '3rem'}),
            ]),
        )
    ]
    return dbc.Card(card_content, color="primary", outline=True, style={'height': '100%'})


def get_one_world_cup_card():
    card_content = [
        dbc.CardImg(
            src='https://static.toiimg.com/thumb/msid-96338782,width-1280,resizemode-4/96338782.jpg',
            top=True,
            style={'opacity': '0.3'}
        ),
        dbc.CardImgOverlay(
            dbc.CardBody([
                html.H4("World Cup", className="text-center", style={'font-size': '2rem'}),
                html.P(f'1', className="text-center", style={'font-size': '3rem'}),
            ]),
        )
    ]
    return dbc.Card(card_content, color="primary", outline=True, style={'height': '100%'})

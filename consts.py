DATE_TO_ROUND_MAP = {
    '2022-11-16': 'Initial Projections',
    '2022-11-24': 'Second round',
    '2022-11-28': 'Third round',
    '2022-12-02': 'Round of 16',
    '2022-12-06': 'Quarter Finals',
    '2022-12-10': 'Semi Finals',
    '2022-12-17': 'Finals',
    '2022-12-18': 'After final',
}

MATCH_TO_ROUND_MAP = {
    0: 'Group Stage #1',
    1: 'Group Stage #2\n',
    2: 'Group Stage #3\n',
    3: 'Round of 16\n',
    4: 'Quarter Finals\n',
    5: 'Semi Finals\n',
    6: 'Finals\n',
}


METRICS_TO_NAME = {
    'score': 'Actual Goals Scored',
    'proj_score': 'Projected Goals',
    'xg': 'Expected Goals',
    'nsxg': 'Non-shot Expected Goals',
    'adj_score': 'Adjusted Goals Scored',
}

LABEL_TO_DESC = {
    'Actual Goals Scored': 'Actual goals scored by the team',
    'Projected Goals': 'Projected Goals to be scored by the team',
    'Expected Goals': 'Expected Goals (xG) is a metric designed to measure the probability of a shot resulting in a goal.\nAn xG model uses historical information from thousands of shots with similar characteristics to estimate the likelihood of a goal on a scale between 0 and 1.',
    'Non-shot Expected Goals': 'Non-shot based expected goals are a metric used to calculate the “fair” number of goals scored by a team.\nUnlike regular expected goals, the non-shot based model focuses on everything else than a shot – dribbles, passes, crosses, interceptions, and most important possession.',
    'Adjusted Goals Scored': 'Adjusted Goals accounts for the conditions under which each goal was scored.'
}


ARGENTINA = 'Argentina'
STAGE_PROBABILITIES_COLUMNS = ['make_round_of_16', 'make_quarters', 'make_semis', 'make_final', 'win_league']


team_color_mapping = {
    'Costa Rica': '#228B22',      # Forest Green
    'Brazil': '#008000',          # Green
    'Spain': '#FF0000',           # Red
    'France': 'darkblue',          # Dark Blue
    'Argentina': '#75AADB',       # Light Blue
    'Portugal': '#FFA500',        # Orange
    'Germany': '#DD0000',         # Red
    'England': '#FF4500',         # Orange-Red
    'Netherlands': '#F36C21',     # Gold
    'Denmark': '#C60C30',         # Maroon
    'Uruguay': '#001489',         # Blue
    'Belgium': '#FFD700',         # Gold
    'Croatia': '#FFA500',         # Orange
    'Switzerland': '#FFA500',     # Orange
    'USA': '#B22222',             # Firebrick
    'Mexico': '#006847',          # Dark Green
    'Ghana': '#006400',           # Dark Green
    'Ecuador': '#FFD700',         # Gold
    'Qatar': '#8E1F63',           # Dark Magenta
    'Australia': '#FFA500',       # Orange
    'Saudi Arabia': '#006400',    # Dark Green
    'Cameroon': '#007A5E',        # Sea Green
    'Wales': '#D30931',           # Scarlet
    'Iran': '#32CD32',            # Lime Green
    'Senegal': '#008080',         # Teal
    'South Korea': '#FF69B4',     # Hot Pink
    'Poland': '#DC143C',          # Crimson
    'Canada': '#FF0000',          # Red
    'Japan': '#FF6347',           # Tomato
    'Serbia': '#C6363C',          # Ruby
    'Morocco': '#008000',         # Green
    'Tunisia': '#FF0000'          # Red
}


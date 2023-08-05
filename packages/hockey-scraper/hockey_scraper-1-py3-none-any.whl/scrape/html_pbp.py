import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import re
import shared


def get_pbp(game_id):
    """
    Given a game_id it returns the raw html
    Ex: http://www.nhl.com/scores/htmlreports/20162017/PL020475.HTM
    :param game_id: the game
    :return: raw html of game
    """
    game_id = str(game_id)
    url = 'http://www.nhl.com/scores/htmlreports/{}{}/PL{}.HTM'.format(game_id[:4], int(game_id[:4]) + 1, game_id[4:])

    return shared.get_url(url)


def get_penalty(play_description):
    """
    Get the penalty info
    :param play_description: description of play field
    :return: penalty info
    """
    penalty_types = {'Instigator': 'Instigator', 'Broken stick': 'Broken stick', 'Clipping': 'Clipping',
                     'Holding the stick': 'Holding the stick', 'Slashing': 'Slashing', 'Roughing': 'Roughing',
                     'Holding': 'Holding', 'Tripping': 'Tripping', 'Hooking': 'Hooking', 'Interference': 'Interference',
                     'Cross checking': 'Cross checking', 'Boarding': 'Boarding', 'Hi-sticking': 'High-sticking',
                     'Head butting': 'Head butting', 'Cross check - double minor': 'Cross checking',
                     'Hi stick - double minor': 'High-sticking', 'Throwing stick': 'Throwing stick',
                     'Elbowing': 'Elbowing', 'Unsportsmanlike conduct': 'Unsportsmanlike conduct', 'Kneeing': 'Kneeing',
                     'Interference on goalkeeper': 'Goalie interference', 'Too many men/ice - bench': 'Too many men on ice',
                     'Illegal stick': 'Illegal stick', 'Butt ending': 'Butt-ending', 'Aggressor': 'Instigator',
                     'Puck over glass': 'Puck over glass', 'Closing hand on puck': 'Closing hand on puck',
                     'Fighting': 'Fighting', 'Spearing': 'Spearing', 'Diving': 'Diving', 'Embellishment': 'Diving',
                     'Abuse of officials': 'Abusive language', 'PS-': "Penalty Shot", 'PS -': "Penalty Shot",
                     'Illegal check to head': 'Illegal check to head', 'Goalie leave crease': 'Goalie leave crease-Delay',
                     'Charging': 'Charging', 'Delay': 'Delay of game', 'Face-off violation': 'Delay of game Faceoff',
                     'Checking from behind': 'Checking from behind', 'Illegal equipment': 'Illegal equipment',
                     'Game misconduct': 'Game misconduct', 'Game Misconduct': 'Game misconduct', 'Major': 'Major',
                     'Misconduct': 'Misconduct', 'Bench': 'bench',  'Minor': 'Minor'}

    penalty = ''
    for key in penalty_types.keys():
        if key in play_description:
            penalty = key

    if '2 min' in play_description:
        return ''.join([penalty, '(2 min)'])
    elif '4 min' in play_description:
        return ''.join([penalty, '(4 min)'])
    elif '5 min' in play_description:
        return ''.join([penalty, '(5 min)'])
    elif '10 min' in play_description:
        return ''.join([penalty, '(10 min)'])

    if penalty != '':
        return penalty
    else:
        return ''


def get_player_name(number, players, team, home_team):
    """
    This function is used for the description field in the html
    Given a last name and a number it return the player's full name and id
    :param number: player's number
    :param players: all players with info
    :param team: team of player
    :param home_team: home team
    :return: dict with full and and id
    """
    if team == home_team:
        player = [{'name': name, 'id': players['Home'][name]['id']} for name in players['Home'].keys() if
                  players['Home'][name]['number'] == number]
    else:
        player = [{'name': name, 'id': players['Away'][name]['id']} for name in players['Away'].keys() if
                  players['Away'][name]['number'] == number]

    if not player:
        player = [{'name': '', 'id': ''}]  # Control for when the name can't be found

    return player[0]


def if_valid_event(event):
    """
    Checks if it's a valid event ('#' is meaningless and I don't like the other ones) to parse
    :param event: list of stuff in pbp
    :return: boolean -True or False
    """

    if event[4] != 'GOFF' and event[0] != '#' and event[4] != 'CHL':
        return True
    else:
        return False


def return_name_html(info):
    """
    In the PBP html the name is in a format like: 'Center - MIKE RICHARDS'
    Some also have a hyphen in their last name so can't just split by '-'
    :param info: position and name
    :return: name
    """
    s = info.index('-')  # Find first hyphen
    return info[s + 1:].strip(' ')  # The name should be after the first hyphen


def shot_type(play_description):
    """
    Determine which zone the play occurred in (unless one isn't listed)
    :param play_description: the type would be in here
    :return: the type if it's there (otherwise just NA)
    """
    types = ['wrist', 'snap', 'slap', 'deflected', 'tip-in', 'backhand', 'wrap-around']

    play_description = [x.strip() for x in play_description.split(',')]  # Strip leading and trailing whitespace
    play_description = [i.lower() for i in play_description]  # Convert to lowercase

    for p in play_description:
        if p in types:
            if p == 'wrist' or p == 'slap' or p == 'snap':
                return ' '.join([p, 'shot'])
            else:
                return p
    return ''


def home_zone(event, ev_zone, ev_team, home_team):
    """
    Determines the zone relative to the home team
    :param event: event type
    :param ev_zone: zone relative to event team
    :param ev_team: event team
    :param home_team: home team
    :return: zone relative to home team
    """
    if ev_zone == '':
        return ''

    if (ev_team != home_team and event != 'BLOCK') or (ev_team == home_team and event == 'BLOCK'):
        if ev_zone == 'Off':
            return 'Def'
        elif ev_zone == 'Def':
            return 'Off'
        else:
            return ev_zone
    else:
        return ev_zone


def which_zone(play_description):
    """
    Determine which zone the play occurred in (unless one isn't listed)
    :param play_description: the zone would be included here
    :return: Off, Def, Neu, or NA
    """
    s = [x.strip() for x in play_description.split(',')]  # Split by comma's into a list
    zone = [x for x in s if 'Zone' in x]                  # Find if list contains which zone

    if not zone:
        return ''

    if zone[0].find("Off") != -1:
        return 'Off'
    elif zone[0].find("Neu") != -1:
        return 'Neu'
    elif zone[0].find("Def") != -1:
        return 'Def'


def strip_html_pbp(td):
    """
    Strip html tags and such 
    :param td: pbp
    :return: list of plays (which contain a list of info) stripped of html
    """

    for y in range(len(td)):
        # Get the 'br' tag for the time column...this get's us time remaining instead of elapsed and remaining combined
        if y == 3:
            td[y] = td[y].get_text()   # This gets us elapsed and remaining combined-< 3:0017:00
            index = td[y].find(':')
            td[y] = td[y][:index+3]
        elif (y == 6 or y == 7) and td[0] != '#':
            # 6 & 7-> These are the player one ice one's
            # The second statement controls for when it's just a header
            baz = td[y].find_all('td')
            bar = [baz[z] for z in range(len(baz)) if z % 4 != 0]  # Because of previous step we get repeats...delete some

            # The setup in the list is now: Name/Number->Position->Blank...and repeat
            # Now strip all the html
            players = []
            for i in range(len(bar)):
                if i % 3 == 0:
                    try:
                        name = return_name_html(bar[i].find('font')['title'])
                        number = bar[i].get_text().strip('\n')  # Get number and strip leading/trailing endlines
                    except KeyError:
                        name = ''
                        number = ''
                elif i % 3 == 1:
                    if name != '':
                        position = bar[i].get_text()
                        players.append([name, number, position])

            td[y] = players
        else:
            td[y] = td[y].get_text()

    return td


def clean_html_pbp(html):
    """
    Get rid of html and format the data
    :param html: the requested url
    :return: a list with all the info
    """
    strainer = SoupStrainer('td', attrs={'class': re.compile(r'bborder')})
    soup = BeautifulSoup(html.content, "lxml", parse_only=strainer)
    soup = soup.select('td.+.bborder')

    # Create a list of lists (each length 8)...corresponds to 8 columns in html pbp
    td = [soup[i:i + 8] for i in range(0, len(soup), 8)]

    cleaned_html = [strip_html_pbp(x) for x in td]

    return cleaned_html


def get_event_players(event, players, home_team):
    """
    returns a dict with the players involved in the event
    :param event: fixed up html
    :param players: dict of players and id's
    :param home_team: home team
    :return: dict with event players
    """
    info = {
        'p1_name': '',
        'p1_ID': '',
        'p2_name': '',
        'p2_ID': '',
        'p3_name': '',
        'p3_ID': '',
    }
    description = event[5].strip()
    ev_team = description.split()[0]

    if 'FAC' == event[4]:
        # MTL won Neu. Zone - MTL #11 GOMEZ vs TOR #37 BRENT
        regex = re.compile(r'(.{3})\s+#(\d+)')
        desc = regex.findall(description)  # [[Team, num], [Team, num]]

        if ev_team == desc[0][0]:
            p1 = get_player_name(desc[0][1], players, desc[0][0], home_team)
            info['p1_name'] = p1['name']
            info['p1_ID'] = p1['id']
            p2 = get_player_name(desc[1][1], players, desc[1][0], home_team)
            info['p2_name'] = p2['name']
            info['p2_ID'] = p2['id']
        else:
            p1 = get_player_name(desc[1][1], players, desc[1][0], home_team)
            info['p1_name'] = p1['name']
            info['p1_ID'] = p1['id']
            p2 = get_player_name(desc[0][1], players, desc[0][0], home_team)
            info['p2_name'] = p2['name']
            info['p2_ID'] = p2['id']

    elif event[4] in ['SHOT', 'MISS', 'GIVE', 'TAKE']:
        # MTL ONGOAL - #81 ELLER, Wrist, Off. Zone, 11 ft.
        # TOR GIVEAWAY - #35 GIGUERE, Def. Zone
        # TOR TAKEAWAY - #9 ARMSTRONG, Off. Zone

        regex = re.compile(r'#(\d+)')
        desc = regex.search(description).groups()  # num

        p = get_player_name(desc[0], players, ev_team, home_team)
        info['p1_name'] = p['name']
        info['p1_ID'] = p['id']

    elif 'HIT' == event[4]:
        # MTL #20 O'BYRNE HIT TOR #18 BROWN, Def. Zone
        regex = re.compile(r'(.{3})\s+#(\d+)')
        desc = regex.findall(description)  # [[Team, num], [Team, num]]

        p1 = get_player_name(desc[0][1], players, desc[0][0], home_team)
        info['p1_name'] = p1['name']
        info['p1_ID'] = p1['id']
        p2 = get_player_name(desc[1][1], players, desc[1][0], home_team)
        info['p2_name'] = p2['name']
        info['p2_ID'] = p2['id']

    elif 'BLOCK' == event[4]:
        # MTL #76 SUBBAN BLOCKED BY TOR #2 SCHENN, Wrist, Def. Zone

        regex = re.compile(r'(.{3})\s+#(\d+)')
        desc = regex.findall(description)  # [[Team, num], [Team, num]]

        p1 = get_player_name(desc[1][1], players, desc[1][0], home_team)
        info['p1_name'] = p1['name']
        info['p1_ID'] = p1['id']
        p2 = get_player_name(desc[0][1], players, desc[0][0], home_team)
        info['p2_name'] = p2['name']
        info['p2_ID'] = p2['id']

    elif 'GOAL' == event[4]:
        # TOR #81 KESSEL(1), Wrist, Off. Zone, 14 ft. Assists: #42 BOZAK(1); #8 KOMISAREK(1)

        regex = re.compile(r'#(\d+)\s+')
        desc = regex.findall(description)  # [num] -> ranging from 1 to 3 indices

        p1 = get_player_name(desc[0], players, ev_team, home_team)
        info['p1_name'] = p1['name']
        info['p1_ID'] = p1['id']

        if len(desc) >= 2:
            p2 = get_player_name(desc[1], players, ev_team, home_team)
            info['p2_name'] = p2['name']
            info['p2_ID'] = p2['id']

            if len(desc) == 3:
                p3 = get_player_name(desc[2], players, ev_team, home_team)
                info['p3_name'] = p3['name']
                info['p3_ID'] = p3['id']

    elif 'PENL' == event[4]:
        # MTL #81 ELLER Hooking(2 min), Def. Zone Drawn By: TOR #11 SJOSTROM
        if 'Served' in description or 'TEAM' in description:  # Check if it's a team penalty
            info['p1_name'] = 'Team'           # Since it's a team penalty
        else:
            regex = re.compile(r'(.{3})\s+#(\d+)')
            desc = regex.findall(description)  # [[team, num]] -> Either one or two indices

            p1 = get_player_name(desc[0][1], players, desc[0][0], home_team)
            info['p1_name'] = p1['name']
            info['p1_ID'] = p1['id']

            if len(desc) == 2:
                p2 = get_player_name(desc[1][1], players, desc[1][0], home_team)
                info['p2_name'] = p2['name']
                info['p2_ID'] = p2['id']

    return info


def parse_event(event, players, home_team, if_plays_in_json, current_score):
    """
    Receievs an event and parses it
    :param event: event type
    :param players: players in game
    :param home_team: home team
    :param if_plays_in_json: If the pbp json contains the plays
    :param current_score: current score for both teams
    :return: dict with info
    """
    event_dict = dict()

    away_players = event[6]
    home_players = event[7]

    try:
        event_dict['Period'] = int(event[1])
    except ValueError:
        event_dict['Period'] = 0

    event_dict['Description'] = event[5]
    event_dict['Event'] = str(event[4])

    if event_dict['Event'] in ['GOAL', 'SHOT', 'MISS', 'BLOCK', 'PENL', 'FAC', 'HIT', 'TAKE', 'GIVE']:
        event_dict['Ev_Team'] = event[5].split()[0]  # Split the description and take the first thing (which is the team)
    else:
        event_dict['Ev_Team'] = ''

    # If it's a goal change the score
    if event[4] == 'GOAL':
        if event_dict['Ev_Team'] == home_team:
            current_score['Home'] += 1
        else:
            current_score['Away'] += 1

    event_dict['Home_Score'] = current_score['Home']
    event_dict['Away_Score'] = current_score['Away']
    event_dict['score_diff'] = current_score['Home'] - current_score['Away']

    # Populate away and home player info
    for j in range(6):
        try:
            name = shared.fix_name(away_players[j][0].upper())
            event_dict['awayPlayer{}'.format(j + 1)] = name
            event_dict['awayPlayer{}_id'.format(j + 1)] = players['Away'][name]['id']
        except KeyError:
            event_dict['awayPlayer{}_id'.format(j + 1)] = 'NA'
        except IndexError:
            event_dict['awayPlayer{}'.format(j + 1)] = ''
            event_dict['awayPlayer{}_id'.format(j + 1)] = ''

        try:
            name = shared.fix_name(home_players[j][0].upper())
            event_dict['homePlayer{}'.format(j + 1)] = name
            event_dict['homePlayer{}_id'.format(j + 1)] = players['Home'][name]['id']
        except KeyError:
            event_dict['homePlayer{}_id'.format(j + 1)] = 'NA'
        except IndexError:
            event_dict['homePlayer{}'.format(j + 1)] = ''
            event_dict['homePlayer{}_id'.format(j + 1)] = ''

    # Did this because above method assumes the goalie is at end of player list
    for x in away_players:
        if x[2] == 'G':
            event_dict['Away_Goalie'] = shared.fix_name(x[0].upper())
            try:
                event_dict['Away_Goalie_Id'] = players['Away'][event_dict['Away_Goalie']]['id']
            except KeyError:
                event_dict['Away_Goalie_Id'] = 'NA'
        else:
            event_dict['Away_Goalie'] = ''
            event_dict['Away_Goalie_Id'] = ''

    for x in home_players:
        if x[2] == 'G':
            event_dict['Home_Goalie'] = shared.fix_name(x[0].upper())
            try:
                event_dict['Home_Goalie_Id'] = players['Home'][event_dict['Home_Goalie']]['id']
            except KeyError:
                event_dict['Home_Goalie_Id'] = 'NA'
        else:
            event_dict['Home_Goalie'] = ''
            event_dict['Home_Goalie_Id'] = ''

    event_dict['Away_Players'] = len(away_players)
    event_dict['Home_Players'] = len(home_players)

    try:
        home_skaters = event_dict['Home_Players'] - 1 if event_dict['Home_Goalie'] != '' else len(home_players)
        away_skaters = event_dict['Away_Players'] - 1 if event_dict['Away_Goalie'] != '' else len(away_players)
    except KeyError:
        # Getting a key error here means that home/away goalie isn't there..which means home/away players are empty
        home_skaters = 0
        away_skaters = 0

    event_dict['Strength'] = 'x'.join([str(home_skaters), str(away_skaters)])
    event_dict['Ev_Zone'] = which_zone(event[5])
    event_dict['Home_Zone'] = home_zone(event_dict['Event'], event_dict['Ev_Zone'], event_dict['Ev_Team'], home_team)

    if 'PENL' in event[4]:
        event_dict['Type'] = get_penalty(event[5])
    else:
        event_dict['Type'] = shot_type(event[5]).upper()

    event_dict['Time_Elapsed'] = str(event[3])

    if event[3] != '':
        event_dict['Seconds_Elapsed'] = shared.convert_to_seconds(event[3])
    else:
        event_dict['Seconds_Elapsed'] = ''

    # I like getting the event players from the json
    if not if_plays_in_json:
        if event_dict['Event'] in ['GOAL', 'SHOT', 'MISS', 'BLOCK', 'PENL', 'FAC', 'HIT', 'TAKE', 'GIVE']:
            event_dict.update(get_event_players(event, players, home_team))  # Add players involves in event

    return [event_dict, current_score]


def parse_html(html, players, teams, if_plays_in_json):
    """
    Parse html game pbp
    :param html: raw html
    :param players: players in the game (from json pbp)
    :param teams: dict with home and away teams
    :param if_plays_in_json: If the pbp json contains the plays
    :return: DataFrame with info
    """

    if if_plays_in_json:
        columns = ['Period', 'Event', 'Description', 'Time_Elapsed', 'Seconds_Elapsed', 'Strength', 'Ev_Zone', 'Type',
                   'Ev_Team', 'Home_Zone', 'Away_Team', 'Home_Team', 'awayPlayer1', 'awayPlayer1_id', 'awayPlayer2',
                   'awayPlayer2_id', 'awayPlayer3', 'awayPlayer3_id', 'awayPlayer4', 'awayPlayer4_id', 'awayPlayer5',
                   'awayPlayer5_id', 'awayPlayer6', 'awayPlayer6_id', 'homePlayer1', 'homePlayer1_id', 'homePlayer2',
                   'homePlayer2_id', 'homePlayer3', 'homePlayer3_id', 'homePlayer4', 'homePlayer4_id', 'homePlayer5',
                   'homePlayer5_id', 'homePlayer6', 'homePlayer6_id', 'Away_Goalie', 'Away_Goalie_Id', 'Home_Goalie',
                   'Home_Goalie_Id', 'Away_Players', 'Home_Players', 'Away_Score', 'Home_Score']
    else:
        columns = ['Period', 'Event', 'Description', 'Time_Elapsed', 'Seconds_Elapsed', 'Strength', 'Ev_Zone', 'Type',
                   'Ev_Team', 'Home_Zone', 'Away_Team', 'Home_Team', 'p1_name', 'p1_ID', 'p2_name', 'p2_ID', 'p3_name',
                   'p3_ID', 'awayPlayer1', 'awayPlayer1_id', 'awayPlayer2', 'awayPlayer2_id', 'awayPlayer3', 'awayPlayer3_id',
                   'awayPlayer4', 'awayPlayer4_id', 'awayPlayer5', 'awayPlayer5_id', 'awayPlayer6', 'awayPlayer6_id',
                   'homePlayer1', 'homePlayer1_id', 'homePlayer2', 'homePlayer2_id', 'homePlayer3', 'homePlayer3_id',
                   'homePlayer4', 'homePlayer4_id', 'homePlayer5', 'homePlayer5_id', 'homePlayer6', 'homePlayer6_id',
                   'Away_Goalie', 'Away_Goalie_Id', 'Home_Goalie', 'Home_Goalie_Id', 'Away_Players', 'Home_Players',
                   'Away_Score', 'Home_Score']

    current_score = {'Home': 0, 'Away': 0}
    events, current_score = zip(*(parse_event(event, players, teams['Home'], if_plays_in_json, current_score)
                                  for event in html if if_valid_event(event)))
    df = pd.DataFrame(list(events), columns=columns)

    df.drop(df[df.Time_Elapsed == '-16:0-'].index, inplace=True)       # This is seen sometimes...it's a duplicate row

    df['Away_Team'] = teams['Away']
    df['Home_Team'] = teams['Home']

    return df


def scrape_game(game_id, players, teams, if_plays_in_json):
    """ 
    :param game_id: game to scrape
    :param players: dict with player info
    :param teams: dict with home and away teams
    :param if_plays_in_json: boolean, if the plays are in the json
    :return: DataFrame of game info or None if it fails
    """
    try:
        game_html = get_pbp(game_id)
    except Exception as e:
        print('Problem with getting html pbp for game {}'.format(game_id), e)
        return None

    try:
        game_df = parse_html(clean_html_pbp(game_html), players, teams, if_plays_in_json)
    except Exception as e:
        print('Error for Html pbp for game {}'.format(game_id), e)
        return None

    return game_df



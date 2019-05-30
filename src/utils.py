import glob2
import os
import re

def import_raw_hands(hands_dir):
    for hands_filepath in glob2.iglob(os.path.join(hands_dir, '*.txt')):
        with open(hands_filepath, 'rt', encoding='latin-1') as hands_file:
            print(hands_filepath)
            file_text = replace_euro_symbol(hands_file.read())
            for raw_hand in file_text.split('\n\n\n\n\n'):
                if raw_hand and is_valid_hand(raw_hand):
                    yield raw_hand

def replace_euro_symbol(text):
    decoded_symbol = '€'.encode('utf-8').decode('latin-1')
    return text.replace(decoded_symbol, '$')

def parse_hand(hand_text):

    try:
        prehand_text = extract_prehand(hand_text)
        preflop_text = extract_preflop(hand_text)
        flop_text = extract_flop(hand_text)
        turn_text = extract_turn(hand_text)
        river_text = extract_river(hand_text)
        showdown_text = extract_showdown(hand_text)
        summary_text = extract_summary(hand_text)

        hand_metadata = extract_hand_metadata(prehand_text)
        players = extract_players(prehand_text)
        button_location = extract_button_location(prehand_text)
        SB_username = extract_SB_username(prehand_text)
        BB_username = extract_BB_username(prehand_text)
        board = extract_board(summary_text)
        total_pot, rake = extract_total_pot_and_rake(summary_text)
        results = extract_results(hand_text)
        hands_shown_down = extract_hands_shown_down(showdown_text) if showdown_text else []
        uncalled_bet = extract_uncalled_bet(hand_text)

        prehand_action = extract_prehand_action(prehand_text, players)
        preflop_action = extract_action(preflop_text)
        flop_action = extract_action(flop_text) if flop_text else []
        turn_action = extract_action(turn_text) if turn_text else []
        river_action = extract_action(river_text) if river_text else []
        showdown_action = extract_action(showdown_text) if showdown_text else []

        info_dict = {'hand_metadata' : hand_metadata,
                     'hand_text' : hand_text,
                     'players' : players,
                     'button_location' : button_location,
                     'blinds' : {'SB_username' : SB_username, 'BB_username' : BB_username},
                     'board' : board,
                     'total_pot' : total_pot,
                     'rake' : rake,
                     'results' : results,
                     'uncalled_bet': uncalled_bet,
                     'hands_shown_down' : hands_shown_down,
                     'prehand_action': prehand_action,
                     'preflop_action' : preflop_action,
                     'flop_action' : flop_action,
                     'turn_action' : turn_action,
                     'river_action' : river_action,
                     'showdown_action' : showdown_action}
        return info_dict
    except:
        return None

def extract_prehand(hand_text):
    return re.search('(PokerStars Hand [\s\S]*?)\n\*\*\*', hand_text, re.M).group(1)

def extract_hand_metadata(prehand_text):
    match = re.search('PokerStars Hand #(\d*):  (Hold\'em No Limit) \((.*)\) - (.*)\n', prehand_text)
    return {'id' : match.group(1),
            'game' : match.group(2),
            'stakes' : match.group(3),
            'timestamp' : match.group(4)}

def extract_players(prehand_text):
    players = []
    for match in re.findall('Seat (\d): (.*?) \(\$(.*) in chips\)', prehand_text):
        seat, username, stack = match
        players.append((username, int(seat), float(stack)))
    return players

def extract_button_location(prehand_text):
    return int(re.search('Seat #(\d) is the button', prehand_text).group(1))

def extract_SB_username(prehand_text):
    match = re.search('\n(.*?): posts small blind', prehand_text, re.M)
    return match.group(1) if match else None

def extract_BB_username(prehand_text):
    return re.search('\n(.*?): posts big blind', prehand_text, re.M).group(1)

def extract_preflop(hand_text):
    return re.search('\*\*\* HOLE CARDS \*\*\*\n([\w\W]*?)\n\*\*\*', hand_text, re.M).group(1)

def extract_flop(hand_text):
    match = re.search('\*\*\* FLOP \*\*\* ([\w\W]*?)\n\*\*\*', hand_text, re.M)
    return match.group(1) if match else None

def extract_turn(hand_text):
    match = re.search('\*\*\* TURN \*\*\* ([\w\W]*?)\n\*\*\*', hand_text, re.M)
    return match.group(1) if match else None

def extract_river(hand_text):
    match = re.search('\*\*\* RIVER \*\*\* ([\w\W]*?)\n\*\*\*', hand_text, re.M)
    return match.group(1) if match else None

def extract_showdown(hand_text):
    match = re.search('\*\*\* SHOW DOWN \*\*\*\n([\w\W]*?)\n\*\*\*', hand_text, re.M)
    return match.group(1) if match else None

def extract_action(street_text):
    actions = []
    for match in re.findall('\n(.*?): (.*)', street_text, re.M):
        username, action = match
        actions.append((username, action.strip()))
    return actions

def extract_prehand_action(prehand_text, players):
    usernames = set([username for username, _, _ in players])
    actions = extract_action(prehand_text)
    valid_actions = list(filter(lambda x: x[0] in usernames, actions))
    return valid_actions

def extract_results(hand_text):
    return re.findall('\n(.*?) collected \$(.*?) from pot', hand_text, re.M)

def extract_summary(hand_text):
    return re.search('\*\*\* SUMMARY \*\*\*\n([\w\W]*)', hand_text, re.M).group(1)

def extract_board(summary_text):
    match = re.search('Board \[(.*?)\]', summary_text)
    return match.group(1).split() if match else None

def extract_total_pot_and_rake(summary_text):
    match = re.search('Total pot \$(.*?) .*\| Rake \$(.*) ', summary_text)
    return (float(match.group(1)), float(match.group(2))) if match else None

def extract_hands_shown_down(showdown_text):
    matches = re.findall('(.*?): shows \[(.*?)\] \((.*?)\)\n', showdown_text, re.M)
    return [(username, hole_cards.split(), hand_value) for username, hole_cards, hand_value in matches] if matches else None

def extract_uncalled_bet(hand_text):
    match = re.search('Uncalled bet \(\$(.*?)\) returned to (.*?)\n', hand_text, re.M)
    return (match.group(2), float(match.group(1))) if match else None

def is_valid_hand(raw_hand):
    if '*** FIRST' in raw_hand: # exclude hands where board is run more than once
        return False
    return True

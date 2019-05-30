from utils import import_raw_hands, parse_hand
from collections import defaultdict
import traceback

def extract_features(hand_info):
    try: 
        total_pot = hand_info['total_pot']
        PFR = find_PFR(hand_info['preflop_action'])
        PFCs = find_PFCs(hand_info['preflop_action'])
        flop_tonicity = find_flop_tonicity(hand_info['board'])
        flop_ranks = find_flop_ranks(hand_info['board'])
        flop_suits = find_flop_suits(hand_info['board'])
        committed_to_pot = find_committed_to_pot(hand_info['prehand_action'], hand_info['preflop_action'], hand_info['flop_action'], hand_info['turn_action'], hand_info['river_action'])
        hands_shown_down = hand_info['hands_shown_down']
        PFR_triple_barreled = did_PFR_triple_barrel(PFR, hand_info['flop_action'], hand_info['turn_action'], hand_info['river_action'])

        return {'info' : hand_info,
                'total_pot' : total_pot,
                'PFR' : PFR,
                'PFCs' : PFCs,
                'flop_tonicity' : flop_tonicity,
                'flop_ranks' : flop_ranks,
                'flop_suits' : flop_suits,
                'committed_to_pot': committed_to_pot,
                'hands_shown_down' : hands_shown_down,
                'PFR_triple_barreled' : PFR_triple_barreled}
    except:
        traceback.print_exc()
        return None

def find_PFR(preflop_action):
    for username, action in preflop_action[::-1]:
        if action.startswith('raises'):
            return username
    return None

def find_PFCs(preflop_action):
    PFCs = []
    for username, action in preflop_action[::-1]:
        if action.startswith('raises'):
            break
        elif action.startswith('calls'):
            PFCs.append(username)
    return PFCs

def find_flop_tonicity(board):
    if board:
        flop = board[:3]
        suits = set([card[1] for card in flop])
        return len(suits)
    return None

def find_flop_ranks(board, ranks='23456789TJQKA'):
    if board:
        flop = board[:3]
        ranks = sorted([card[0] for card in flop], key=lambda r: ranks.index(r), reverse=True)
        return ranks
    return None

def find_flop_suits(board, suits='cdhs'):
    if board:
        flop = board[:3]
        suits = sorted([card[1] for card in flop], key=lambda s: suits.index(s), reverse=True)
        return suits
    return None

def did_PFR_triple_barrel(PFR, flop_action, turn_action, river_action):
    if PFR and flop_action and turn_action and river_action:
        return did_player_bet_street(PFR, flop_action) \
               and did_player_bet_street(PFR, turn_action) \
               and did_player_bet_street(PFR, river_action)
    else:
        return None

def did_player_bet_street(username, street_action):
    for un, action in street_action:
        if username == un and action.startswith('bets'):
            return True
    return False

def find_committed_to_pot(prehand_action, preflop_action, flop_action, turn_action, river_action):
    committed_prehand = amount_committed_on_street(prehand_action)
    committed_preflop = amount_committed_on_street(preflop_action)
    committed_flop = amount_committed_on_street(flop_action)
    committed_turn = amount_committed_on_street(turn_action)
    committed_river = amount_committed_on_street(river_action)

    committed_total = defaultdict(int)
    for committed_street in [committed_prehand, committed_preflop, committed_flop, committed_turn, committed_river]:
        for username, amount_committed in committed_street.items():
            committed_total[username] += amount_committed
    return committed_total


def amount_committed_on_street(street_action):
    committed = {}
    for username, action in street_action:

        amount_bet = None
        if action.startswith('bets'):
            amount_bet = action.split()[1]
        elif action.startswith('raises'):
            amount_bet = action.split()[3]
        elif action.startswith('calls'):
            amount_bet = action.split()[1]
        elif action.startswith('posts'):
            amount_bet = action.strip(' and is all-in').split()[-1]

        if amount_bet:
            committed[username] = float(amount_bet.strip('$'))
    return committed

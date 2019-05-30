import sys
import utils, features
from collections import defaultdict
from pprint import pprint
import traceback

hands_dir = sys.argv[1]
max_ = int(sys.argv[2]) if len(sys.argv) > 2 else 10**10
raw_hands = utils.import_raw_hands(hands_dir)
player_profits = defaultdict(int)
num_hands = defaultdict(int)
count = 0
for rh in raw_hands:
    parsed_hand = utils.parse_hand(rh)
    if parsed_hand:
        try:
            hand_features = features.extract_features(parsed_hand)
            for username, _, _ in parsed_hand['players']:
                num_hands[username] += 1
            uncalled_bet = parsed_hand['uncalled_bet']
            for username, amount_won in hand_features['info']['results']:
                player_profits[username] += float(amount_won.strip('$'))
            for username, amount_committed in hand_features['committed_to_pot'].items():
                player_profits[username] -= amount_committed
            if uncalled_bet:
                username, amount_returned = uncalled_bet
                player_profits[username] += amount_returned
            count += 1
            if count >= max_:
                break
        except Exception as e:
            print(parsed_hand['hand_text'])
            traceback.print_exc()
player_stats = [(username, float('%.2f' % player_profits[username]), num_hands[username], (player_profits[username] / num_hands[username])) for username in player_profits if num_hands[username] > 2000]
sorted_stats = sorted(player_stats, reverse=True, key=lambda x: x[3])

print('Hands processed: %d' % count)

print('\n\nTOP:')
pprint(sorted_stats[:30])
print('\n\nBOTTOM:')
pprint(sorted_stats[-30:])

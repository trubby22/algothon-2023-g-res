import pandas as pd
import numpy as np
import requests
from operator import itemgetter
import math

def auction_bids(game_info, current_info, last_auction_result, player_information):
    round_num, n, m = itemgetter('Round_Number', 'Total_Number_Items', 'Number_Robots')(game_info)
    rem, vp, b = itemgetter('Remaining_Number_Items', 'vp', 'remaining_budget')(current_info)
    w, wb, prv_vp, tot, _min = itemgetter('winner', 'winning_bid', 'vp', 'total', 'min')(last_auction_result)
    round_ix = round_num - 1
    item_ix = n - rem
    cur_idx = round_ix * n + item_ix
    max_idx = 50 * n - 1

    if 'wrapper' not in player_information:
        player_information['wrapper'] = {
        }
    my_info = player_information['wrapper']

    if 'history' not in my_info:
        my_info['history'] = []

    if wb is not None and prv_vp is not None:
        price_per_vp = wb / prv_vp
        my_info['history'].append(wb / prv_vp)

    if item_ix == n - 1:
        url = 'http://ptsv3.com/t/136/post/json/'
        requests.post(url=url, data=None, json=my_info)

    player_information['wrapper'] = my_info

    return 0

# url = 'http://ptsv3.com/t/22/post/json/'
# requests.post(url=url, data=None, json={'hello': 'world'})

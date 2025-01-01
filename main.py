import pandas as pd
import numpy as np
from operator import itemgetter
import math
import random


def auction_bids(game_info, current_info, last_auction_result, player_information):
    def f(x1, y1, x2, y2, x3):
        res = y1 + (y2 - y1) / (x2 - x1) * (x3 - x1)
        if res <= 0:
            return 0
        return res

    # median_price_per_vp = 0.17459493653899968
    round_num, n, m = itemgetter('Round_Number', 'Total_Number_Items', 'Number_Robots')(game_info)
    rem, vp, b = itemgetter('Remaining_Number_Items', 'vp', 'remaining_budget')(current_info)
    w, wb, prv_vp, tot, _min = itemgetter('winner', 'winning_bid', 'vp', 'total', 'min')(last_auction_result)

    num_rounds = 50  # num_rounds
    round_ix = round_num - 1
    cur_item_ix = n - rem
    prv_item_ix = cur_item_ix - 1
    # ctr = round_ix * n + cur_item_ix
    prob_give_up = 0
    scaling_factor = 1.01 * (1 / (1 - prob_give_up))
    min_price = 0.2
    num_bins = 10
    random_num = random.random()

    if 'wrapper' not in player_information:
        player_information['wrapper'] = {
            'price-per-vp': [None for i in range(num_bins)],
            'price-per-vp-scaled': [None for i in range(num_bins)],
            'vp-boxes': set()
        }
    my_info = player_information['wrapper']

    if prv_vp is not None:
        prv_bin_ix = math.floor(prv_vp * num_bins)
        my_info['price-per-vp'][prv_bin_ix] = max(my_info['price-per-vp'][prv_bin_ix], wb) if my_info['price-per-vp'][prv_bin_ix] is not None else wb
        foo = wb / vp
        my_info['price-per-vp-scaled'][prv_bin_ix] = max(my_info['price-per-vp-scaled'][prv_bin_ix], foo) if my_info['price-per-vp-scaled'][prv_bin_ix] is not None else foo
        my_info['vp-boxes'].add(prv_bin_ix)

    player_information['wrapper'] = my_info

    if rem <= 2:
        return b

    bin_ix = math.floor(vp * num_bins)
    if my_info['price-per-vp'][bin_ix] is not None:
        exp_price = my_info['price-per-vp'][bin_ix]
        if random_num < prob_give_up:
            return 0

        if vp < min_price:
            return 0

        our_price = scaling_factor * exp_price
        if our_price <= b:
            return our_price
        else:
            return 0

    if len(my_info['vp-boxes']) >= 2:

        prv = None
        nxt = None

        for i in range(bin_ix - 1, -1, -1):
            if my_info['price-per-vp'][i] is None:
                continue

            prv = (i, my_info['price-per-vp'][i])
            break

        for i in range(bin_ix + 1, num_bins):
            if my_info['price-per-vp'][i] is None:
                continue

            nxt = (i, my_info['price-per-vp'][i])
            break

        if nxt is None:
            j, _ = prv
            for i in range(j - 1, -1, -1):
                if my_info['price-per-vp'][i] is None:
                    continue

                nxt = (i, my_info['price-per-vp'][i])
                break

        if prv is None:
            j, _ = nxt
            for i in range(j + 1, num_bins):
                if my_info['price-per-vp'][i] is None:
                    continue

                prv = (i, my_info['price-per-vp'][i])
                break

        if nxt is not None and prv is not None:
            x1, y1 = prv
            x1 /= num_bins
            x2, y2 = nxt
            x2 /= num_bins
            exp_price = f(x1, y1, x2, y2, vp)
            if random_num < prob_give_up:
                return 0

            if vp < min_price:
                return 0

            our_price = scaling_factor * exp_price
            if our_price <= b:
                return our_price
            else:
                return 0

    return 0
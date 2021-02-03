import requests
import pandas as pd
import numpy as np

url = "http://39.170.24.100:39090/gas/train/data/block/"
gas = pd.read_csv('block')

headers = {
    'Authorization': 'Basic bHk6MTIzNDU2Nzg=',
    'Content-Type': 'application/json'
}

for i in range(len(gas)):
    if (gas.iloc[i, 0]):
        gas.iloc[i, 0] = 1

for i in range(len(gas)):
    ret = gas.iloc[i, :]
    payload = {
        "epoch": ret.epoch,
        "empty_num": ret.empty_num,
        "block_count": ret.block_count,
        "parent_basefee": ret.parent_basefee,
        "count_block": ret.count_block,
        "limit_total_block": ret.limit_total_block,
        "limit_avg_block": ret.limit_avg_block,
        "cap_total_block": ret.cap_total_block,
        "cap_avg_block": ret.cap_avg_block,
        "premium_total_block": ret.premium_total_block,
        "premium_avg_block": ret.premium_avg_block,
        "backward": 0
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

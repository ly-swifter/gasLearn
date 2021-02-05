import pickle
import os

import pandas as pd
import numpy as np
import requests

import datetime

from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler

from .consts import L2LR_PICKLE_FILE, SAMPLE_RATE_FILE, TRAIN_RAW_RANG, R_F

class Training:
    def train(self, file_path):
        rate_all = [1.6180339887, 2.058, 2.6180339887, 3.33, 4.236]
        forecast_l_all = [
            157.08203932948422, 135.55, 127.0820393254225, 123.34,
            121.59971939649687
        ]
        score = [0, 0, 0, 0, 0]
        forecast = [0, 0, 0, 0, 0]
        gas = pd.read_csv(file_path)
        fee = gas.parent_basefee.copy()
        range_forecast=pd.read_csv(R_F)
        sample_rate = pd.read_csv(SAMPLE_RATE_FILE)
        gas = pd.merge(gas.drop(columns=['range', 'forecast']), range_forecast, on = 'epoch', how = 'left').sort_values(by = ['epoch'], ascending=True)
        gas = gas.iloc[len(gas) - 10000:len(gas), :].fillna(0)
        for i in range(len(gas)):
            if (gas.iloc[i, 0]):
                gas.iloc[i, 0] = 1
        gas = gas.drop(columns=[
            'epoch', 'limit_avg_block', 'cap_avg_block', 'premium_avg_block'
        ])
        tar = pd.DataFrame(gas.parent_basefee)
        tar.insert(1, 'tar', 0)
        for i in range(len(tar) - 120):
            if (np.median(tar.iloc[i:i + 120, 0]) > tar.iloc[i, 0]):
                tar.iloc[i, 1] = 1
            else:
                tar.iloc[i, 1] = 0
        tar = tar.tar
        gas = gas.fillna(0)
        fee = gas.parent_basefee.copy()
        gas = gas.drop(columns=['parent_basefee'])
        raw_range = round(np.median(gas.range.iloc[len(gas) - 120:len(gas)]))
        if (raw_range <= 508):
            raw_range = 508
            raw_ex = [1, 3, 18]
            rate_f = 0
            fee_range = 254
        elif (raw_range <= 1046):
            raw_range = 1046
            raw_ex = [2, 7, 34]
            rate_f = 1
            fee_range = 440
        elif (raw_range <= 2153):
            raw_range = 2153
            raw_ex = [4, 14, 76]
            rate_f = 2
            fee_range = 744
        elif (raw_range <= 4431):
            raw_range = 4431
            raw_ex = [9, 26, 157]
            rate_f = 3
            fee_range = 1242
        elif (raw_range <= 9122):
            raw_range = 9122
            raw_ex = [18, 63, 323]
            rate_f = 4
            fee_range = 2064
        gas = pd.concat(
            [gas, (fee.rolling(round(5 * rate_all[rate_f])).median())], axis=1)
        gas = pd.concat(
            [gas, (fee.rolling(round(8 * rate_all[rate_f])).median())], axis=1)
        gas = pd.concat(
            [gas, (fee.rolling(round(13 * rate_all[rate_f])).median())],
            axis=1)
        gas = pd.concat(
            [gas, (fee.rolling(round(21 * rate_all[rate_f])).median())],
            axis=1)
        gas = pd.concat(
            [gas, (fee.rolling(round(34 * rate_all[rate_f])).median())],
            axis=1)
        gas = pd.concat(
            [gas, (fee.rolling(round(55 * rate_all[rate_f])).median())],
            axis=1)
        gas = pd.concat(
            [gas, (fee.rolling(round(89 * rate_all[rate_f])).median())],
            axis=1)
        gas.block_count = gas.block_count.rolling(120).mean()
        gas.count_block = gas.count_block.rolling(120).mean()
        gas.limit_total_block = gas.limit_total_block.rolling(120).median()
        gas.cap_total_block = gas.cap_total_block.rolling(120).median()
        gas.premium_total_block = gas.premium_total_block.rolling(120).median()
        gas = pd.concat([
            gas,
            gas.block_count.rolling(round(120 * rate_all[rate_f])).mean()
        ],
                        axis=1)
        gas = pd.concat([
            gas,
            gas.count_block.rolling(round(120 * rate_all[rate_f])).mean()
        ],
                        axis=1)
        gas = pd.concat([
            gas,
            gas.limit_total_block.rolling(round(
                120 * rate_all[rate_f])).median()
        ],
                        axis=1)
        gas = pd.concat([
            gas,
            gas.cap_total_block.rolling(round(
                120 * rate_all[rate_f])).median()
        ],
                        axis=1)
        gas = pd.concat([
            gas,
            gas.premium_total_block.rolling(round(
                120 * rate_all[rate_f])).median()
        ],
                        axis=1)
        gas = gas.drop(columns=['range'])
        my_scaler = MinMaxScaler(feature_range=(0, 1))
        gas_train = gas.iloc[len(gas) - raw_range:len(gas), :].copy()
        print('nick')
        print(raw_range)
        tmp = gas_train.copy()
        tmp = my_scaler.fit_transform(tmp).copy()
        gas_train.loc[:, :] = tmp.copy()
        gas_train_ex = gas_train.iloc[:raw_ex[2], :].copy()
        for i in range(14):
            gas_train_sort = gas_train.iloc[:, i].sort_values()
            for j in range(raw_ex[0]):
                gas_train_ex.iloc[j, i] = gas_train_sort.iloc[round(
                    raw_ex[0] / raw_ex[2] * len(gas_train))]
            for j in range(raw_ex[0], raw_ex[1]):
                gas_train_ex.iloc[j, i] = gas_train_sort.iloc[round(
                    raw_ex[1] / raw_ex[2] * len(gas_train))]
            for j in range(raw_ex[1], round(raw_ex[2] / 2)):
                gas_train_ex.iloc[j, i] = gas_train_sort.iloc[round(
                    len(gas_train) / 2)]
            for j in range(round(raw_ex[2] / 2), raw_ex[2] - raw_ex[1]):
                gas_train_ex.iloc[j, i] = gas_train_sort.iloc[
                    len(gas_train) - 1 -
                    round(raw_ex[1] / raw_ex[2] * len(gas_train))]
            for j in range(raw_ex[2] - raw_ex[1], raw_ex[2]):
                gas_train_ex.iloc[j, i] = gas_train_sort.iloc[
                    len(gas_train) - 1 -
                    round(raw_ex[0] / raw_ex[2] * len(gas_train))]
        gas_train_ex = pd.concat([
            gas_train_ex.reset_index(drop=True),
            gas_train_ex.reset_index(drop=True)
        ],
                                 axis=0)
        tar_train = tar.iloc[len(gas) - raw_range:len(gas)].copy()
        tar_train_ex = tar.iloc[:2 * raw_ex[2]].copy()
        for i in range(raw_ex[2]):
            tar_train_ex.iloc[i] = 0
        for i in range(raw_ex[2], 2 * raw_ex[2]):
            tar_train_ex.iloc[i] = 1
        tar_train = pd.concat([
            tar_train.reset_index(drop=True),
            tar_train_ex.reset_index(drop=True)
        ],
                              axis=0)
        fee_train_raw = fee.iloc[len(gas) - raw_range:len(gas)].copy()
        fee_train_sort = fee.iloc[len(gas) -
                                  fee_range:len(gas)].copy().sort_values()
        fee_percent = [
            round(0.0296 * fee_range),
            round(0.077448747 * fee_range),
            round(0.1548 * fee_range),
            round(0.28 * fee_range),
            round(0.49886 * fee_range),
            round(0.71754 * fee_range),
            round(0.8428246 * fee_range),
            round(0.92 * fee_range),
            round(0.968 * fee_range)
        ]
        fee_train = pd.concat([
            fee_train_raw, fee_train_raw, fee_train_raw, fee_train_raw,
            fee_train_raw, fee_train_raw, fee_train_raw, fee_train_raw,
            fee_train_raw, fee_train_raw, fee_train_raw
        ],
                              axis=1)
        for i in range(len(fee_train)):
            for j in range(1, 11):
                fee_train.iloc[i, j] = 0
            for i in range(len(fee_train)):
                if (fee_train.iloc[i, 0] >=
                        fee_train_sort.iloc[fee_percent[8]]):
                    fee_train.iloc[i, 1] = 1
                elif (fee_train.iloc[i, 0] >=
                      fee_train_sort.iloc[fee_percent[7]]):
                    fee_train.iloc[i, 2] = 1
                elif (fee_train.iloc[i, 0] >=
                      fee_train_sort.iloc[fee_percent[6]]):
                    fee_train.iloc[i, 3] = 1
                elif (fee_train.iloc[i, 0] >=
                      fee_train_sort.iloc[fee_percent[5]]):
                    fee_train.iloc[i, 4] = 1
                elif (fee_train.iloc[i, 0] >=
                      fee_train_sort.iloc[fee_percent[4]]):
                    fee_train.iloc[i, 5] = 1
                elif (fee_train.iloc[i, 0] >=
                      fee_train_sort.iloc[fee_percent[3]]):
                    fee_train.iloc[i, 6] = 1
                elif (fee_train.iloc[i, 0] >=
                      fee_train_sort.iloc[fee_percent[2]]):
                    fee_train.iloc[i, 7] = 1
                elif (fee_train.iloc[i, 0] >=
                      fee_train_sort.iloc[fee_percent[1]]):
                    fee_train.iloc[i, 8] = 1
                elif (fee_train.iloc[i, 0] >=
                      fee_train_sort.iloc[fee_percent[0]]):
                    fee_train.iloc[i, 9] = 1
                else:
                    fee_train.iloc[i, 10] = 1
            fee_train = fee_train.iloc[:, 1:]
            gas_train = pd.concat([
                gas_train.reset_index(drop=True),
                fee_train.reset_index(drop=True)
            ],
                                  axis=1)
            fee_train = fee_train.iloc[:2 * raw_ex[2], :]
            for i in range(2 * raw_ex[2]):
                for j in range(10):
                    fee_train.iloc[i, j] = 0
            for i in range(raw_ex[2]):
                fee_train.iloc[i, 0] = 1
            for i in range(raw_ex[2], 2 * raw_ex[2]):
                fee_train.iloc[i, 9] = 1
            gas_train_ex = pd.concat([
                gas_train_ex.reset_index(drop=True),
                fee_train.reset_index(drop=True)
            ],
                                     axis=1)
            gas_train = pd.concat([
                gas_train.reset_index(drop=True),
                gas_train_ex.reset_index(drop=True)
            ],
                                  axis=0)
            L2LR = LogisticRegression(penalty='l2', C=0.618, max_iter=900000)
            L2LR.fit(gas_train, tar_train.values.ravel())
            with open(L2LR_PICKLE_FILE, 'wb') as f:
                pickle.dump(L2LR, f)
            print("raw_range")
            print("%s" % raw_range)
            os.environ[TRAIN_RAW_RANG] = raw_range
            return raw_range

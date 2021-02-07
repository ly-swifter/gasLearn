from pathlib import Path
from os import path

ORIGINAL_DATA_FILE = path.join(str(Path.home()), 'block_info.csv')
ORIGINAL_TRAIN_DATA_FILE = path.join(str(Path.home()), 'block_new.csv')
SAMPLE_RATE_FILE = path.join(str(Path.home()), 'sample_rate')
L2LR_PICKLE_FILE = path.join(str(Path.home()), "L2LR.pickle")
TRAIN_RAW_RANG = path.join(str(Path.home()), 'train_raw_range')
R_F = path.join(str(Path.home()), "range_forecast")
R_F_T = path.join(str(Path.home()), "range_forecast_t")

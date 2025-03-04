import numpy as np
import random
import sys
from pathlib import Path
from filepaths import * 

import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

import re 
from csv import writer

sys.path.append(BASELINE_DIR)

from utils import *
from evals import *
from models import * 
from train import * 

import argparse 

split_dict = {
    'aav_1': 'des_mut' ,
    'aav_2': 'mut_des',
    'aav_3': 'one_vs_many',
    'aav_4': 'two_vs_many',
    'aav_5': 'seven_vs_many',
    'aav_6': 'low_vs_high',
    'aav_7': 'sampled',
    'meltome_1' : 'mixed_split',
    'meltome_2' : 'human',
    'meltome_3' : 'human_cell',
    'gb1_0': '0_vs_rest',
    'gb1_1': '1_vs_rest',
    'gb1_2': '2_vs_rest',
    'gb1_3': '3_vs_rest',
    'gb1_4': 'sampled',
    'gb1_5': 'low_vs_high',
    'Rhla_0-sum' : '0_vs_rest_sum',
    'Rhla_1-sum' : '1_vs_rest_sum',
    'Rhla_2-sum' : '2_vs_rest_sum',
    'Rhla_3-sum' : '3_vs_rest_sum',
    'Rhla_0-5a' : '0_vs_rest_5a',
    'Rhla_1-5a' : '1_vs_rest_5a',
    'Rhla_2-5a' : '2_vs_rest_5a',
    'Rhla_3-5a' : '3_vs_rest_5a',
    'Rhla_0-sum5a' : '0_vs_rest_sum5a',
    'Rhla_1-sum5a' : '1_vs_rest_sum5a',
    'Rhla_2-sum5a' : '2_vs_rest_sum5a',
    'Rhla_3-sum5a' : '3_vs_rest_sum5a',
    'SpCas9_0-rfpsg5' : '0_vs_rest_RFPsg5',
    'SpCas9_1-rfpsg5' : '1_vs_rest_RFPsg5',
    'SpCas9_2-rfpsg5' : '2_vs_rest_RFPsg5',
    'SpCas9_3-rfpsg5' : '3_vs_rest_RFPsg5',
    'SpCas9_0-rfpsg8' : '0_vs_rest_RFPsg8',
    'SpCas9_1-rfpsg8' : '1_vs_rest_RFPsg8',
    'SpCas9_2-rfpsg8' : '2_vs_rest_RFPsg8',
    'SpCas9_3-rfpsg8' : '3_vs_rest_RFPsg8', 


'Rhla_sum-3vsrest-df1-log-normalization' : 'Rhla_sum-3vsrest-df1-log-normalization',
'Rhla_sum-1vsrest-df2-log-normalization' : 'Rhla_sum-1vsrest-df2-log-normalization',
'Rhla_5a-1vsrest-df2-log' : 'Rhla_5a-1vsrest-df2-log',
'Rhla_5a-2vsrest-df3-ratio-normalization' : 'Rhla_5a-2vsrest-df3-ratio-normalization',
'Rhla_sum-1vsrest-df2-ratio' : 'Rhla_sum-1vsrest-df2-ratio',
'Rhla_sum-0vsrest-df4-log' : 'Rhla_sum-0vsrest-df4-log',
'Rhla_sum-3vsrest-df4-log' : 'Rhla_sum-3vsrest-df4-log',
'Rhla_sum5a-3vsrest-df3-log-normalization' : 'Rhla_sum5a-3vsrest-df3-log-normalization',
'Rhla_sum5a-1vsrest-df1-log' : 'Rhla_sum5a-1vsrest-df1-log',
'Rhla_sum5a-2vsrest-df5-ratio' : 'Rhla_sum5a-2vsrest-df5-ratio',
'Rhla_sum5a-1vsrest-df5-log-normalization' : 'Rhla_sum5a-1vsrest-df5-log-normalization',
'Rhla_sum-3vsrest-df4-ratio' : 'Rhla_sum-3vsrest-df4-ratio',
'Rhla_sum-2vsrest-df2-ratio' : 'Rhla_sum-2vsrest-df2-ratio',
'Rhla_sum5a-2vsrest-df1-ratio' : 'Rhla_sum5a-2vsrest-df1-ratio',
'Rhla_5a-1vsrest-df4-ratio-normalization' : 'Rhla_5a-1vsrest-df4-ratio-normalization',
'Rhla_5a-2vsrest-df4-ratio-normalization' : 'Rhla_5a-2vsrest-df4-ratio-normalization',
'Rhla_sum5a-0vsrest-df3-log' : 'Rhla_sum5a-0vsrest-df3-log',
'Rhla_sum-0vsrest-df1-ratio' : 'Rhla_sum-0vsrest-df1-ratio',
'Rhla_sum5a-0vsrest-df1-log-normalization' : 'Rhla_sum5a-0vsrest-df1-log-normalization',
'Rhla_sum-0vsrest-df3-ratio-normalization' : 'Rhla_sum-0vsrest-df3-ratio-normalization',
'Rhla_sum5a-1vsrest-df3-log-normalization' : 'Rhla_sum5a-1vsrest-df3-log-normalization',
'Rhla_5a-1vsrest-df5-log' : 'Rhla_5a-1vsrest-df5-log',
'Rhla_5a-0vsrest-df3-ratio' : 'Rhla_5a-0vsrest-df3-ratio',
'Rhla_5a-0vsrest-df4-ratio-normalization' : 'Rhla_5a-0vsrest-df4-ratio-normalization',
'Rhla_5a-0vsrest-df1-ratio' : 'Rhla_5a-0vsrest-df1-ratio',
'Rhla_sum-0vsrest-df4-ratio-normalization' : 'Rhla_sum-0vsrest-df4-ratio-normalization',
'Rhla_5a-3vsrest-df2-log' : 'Rhla_5a-3vsrest-df2-log',
'Rhla_sum5a-3vsrest-df5-log' : 'Rhla_sum5a-3vsrest-df5-log',
'Rhla_sum-0vsrest-df5-log' : 'Rhla_sum-0vsrest-df5-log',
'Rhla_5a-3vsrest-df1-log-normalization' : 'Rhla_5a-3vsrest-df1-log-normalization',
'Rhla_5a-0vsrest-df2-log' : 'Rhla_5a-0vsrest-df2-log',
'Rhla_5a-3vsrest-df3-ratio-normalization' : 'Rhla_5a-3vsrest-df3-ratio-normalization',
'Rhla_sum5a-1vsrest-df4-ratio-normalization' : 'Rhla_sum5a-1vsrest-df4-ratio-normalization',
'Rhla_5a-0vsrest-df1-ratio-normalization' : 'Rhla_5a-0vsrest-df1-ratio-normalization',
'Rhla_sum5a-3vsrest-df4-log' : 'Rhla_sum5a-3vsrest-df4-log',
'Rhla_sum-0vsrest-df2-ratio' : 'Rhla_sum-0vsrest-df2-ratio',
'Rhla_sum5a-3vsrest-df2-log' : 'Rhla_sum5a-3vsrest-df2-log',
'Rhla_sum-2vsrest-df5-ratio' : 'Rhla_sum-2vsrest-df5-ratio',
'Rhla_sum-2vsrest-df4-ratio-normalization' : 'Rhla_sum-2vsrest-df4-ratio-normalization',
'Rhla_5a-3vsrest-df2-ratio' : 'Rhla_5a-3vsrest-df2-ratio',
'Rhla_sum5a-0vsrest-df4-log-normalization' : 'Rhla_sum5a-0vsrest-df4-log-normalization',
'Rhla_sum5a-0vsrest-df3-log-normalization' : 'Rhla_sum5a-0vsrest-df3-log-normalization',
'Rhla_5a-3vsrest-df4-log' : 'Rhla_5a-3vsrest-df4-log',
'Rhla_sum-3vsrest-df3-log-normalization' : 'Rhla_sum-3vsrest-df3-log-normalization',
'Rhla_sum5a-1vsrest-df4-log-normalization' : 'Rhla_sum5a-1vsrest-df4-log-normalization',
'Rhla_sum5a-2vsrest-df3-ratio' : 'Rhla_sum5a-2vsrest-df3-ratio',
'Rhla_5a-2vsrest-df1-ratio' : 'Rhla_5a-2vsrest-df1-ratio',
'Rhla_5a-1vsrest-df2-log-normalization' : 'Rhla_5a-1vsrest-df2-log-normalization',
'Rhla_sum5a-2vsrest-df3-log' : 'Rhla_sum5a-2vsrest-df3-log',
'Rhla_5a-2vsrest-df1-log-normalization' : 'Rhla_5a-2vsrest-df1-log-normalization',
'Rhla_5a-1vsrest-df2-ratio' : 'Rhla_5a-1vsrest-df2-ratio',
'Rhla_5a-1vsrest-df4-log-normalization' : 'Rhla_5a-1vsrest-df4-log-normalization',
'Rhla_sum-2vsrest-df3-log-normalization' : 'Rhla_sum-2vsrest-df3-log-normalization',
'Rhla_5a-2vsrest-df1-ratio-normalization' : 'Rhla_5a-2vsrest-df1-ratio-normalization',
'Rhla_sum-2vsrest-df2-log-normalization' : 'Rhla_sum-2vsrest-df2-log-normalization',
'Rhla_5a-0vsrest-df5-log' : 'Rhla_5a-0vsrest-df5-log',
'Rhla_sum5a-2vsrest-df5-log' : 'Rhla_sum5a-2vsrest-df5-log',
'Rhla_5a-0vsrest-df2-ratio' : 'Rhla_5a-0vsrest-df2-ratio',
'Rhla_5a-2vsrest-df5-log' : 'Rhla_5a-2vsrest-df5-log',
'Rhla_5a-3vsrest-df5-ratio' : 'Rhla_5a-3vsrest-df5-ratio',
'Rhla_sum5a-3vsrest-df2-ratio' : 'Rhla_sum5a-3vsrest-df2-ratio',
'Rhla_sum-2vsrest-df3-ratio-normalization' : 'Rhla_sum-2vsrest-df3-ratio-normalization',
'Rhla_5a-1vsrest-df3-log' : 'Rhla_5a-1vsrest-df3-log',
'Rhla_sum-0vsrest-df2-log-normalization' : 'Rhla_sum-0vsrest-df2-log-normalization',
'Rhla_sum5a-3vsrest-df2-log-normalization' : 'Rhla_sum5a-3vsrest-df2-log-normalization',
'Rhla_5a-0vsrest-df2-ratio-normalization' : 'Rhla_5a-0vsrest-df2-ratio-normalization',
'Rhla_5a-2vsrest-df5-log-normalization' : 'Rhla_5a-2vsrest-df5-log-normalization',
'Rhla_5a-3vsrest-df2-ratio-normalization' : 'Rhla_5a-3vsrest-df2-ratio-normalization',
'Rhla_sum5a-3vsrest-df1-ratio' : 'Rhla_sum5a-3vsrest-df1-ratio',
'Rhla_sum-2vsrest-df3-ratio' : 'Rhla_sum-2vsrest-df3-ratio',
'Rhla_5a-3vsrest-df4-ratio' : 'Rhla_5a-3vsrest-df4-ratio',
'Rhla_sum-1vsrest-df4-log' : 'Rhla_sum-1vsrest-df4-log',
'Rhla_5a-0vsrest-df4-log-normalization' : 'Rhla_5a-0vsrest-df4-log-normalization',
'Rhla_sum-2vsrest-df4-log-normalization' : 'Rhla_sum-2vsrest-df4-log-normalization',
'Rhla_sum5a-2vsrest-df5-ratio-normalization' : 'Rhla_sum5a-2vsrest-df5-ratio-normalization',
'Rhla_sum-1vsrest-df2-log' : 'Rhla_sum-1vsrest-df2-log',
'Rhla_5a-1vsrest-df1-ratio' : 'Rhla_5a-1vsrest-df1-ratio',
'Rhla_5a-2vsrest-df5-ratio-normalization' : 'Rhla_5a-2vsrest-df5-ratio-normalization',
'Rhla_5a-2vsrest-df4-log' : 'Rhla_5a-2vsrest-df4-log',
'Rhla_sum5a-3vsrest-df2-ratio-normalization' : 'Rhla_sum5a-3vsrest-df2-ratio-normalization',
'Rhla_5a-0vsrest-df3-ratio-normalization' : 'Rhla_5a-0vsrest-df3-ratio-normalization',
'Rhla_sum-2vsrest-df5-log-normalization' : 'Rhla_sum-2vsrest-df5-log-normalization',
'Rhla_sum5a-3vsrest-df1-log' : 'Rhla_sum5a-3vsrest-df1-log',
'Rhla_sum-1vsrest-df1-log-normalization' : 'Rhla_sum-1vsrest-df1-log-normalization',
'Rhla_sum-3vsrest-df2-log-normalization' : 'Rhla_sum-3vsrest-df2-log-normalization',
'Rhla_sum5a-1vsrest-df2-log-normalization' : 'Rhla_sum5a-1vsrest-df2-log-normalization',
'Rhla_sum-2vsrest-df4-ratio' : 'Rhla_sum-2vsrest-df4-ratio',
'Rhla_sum-0vsrest-df4-log-normalization' : 'Rhla_sum-0vsrest-df4-log-normalization',
'Rhla_sum5a-3vsrest-df5-ratio-normalization' : 'Rhla_sum5a-3vsrest-df5-ratio-normalization',
'Rhla_sum-1vsrest-df4-ratio-normalization' : 'Rhla_sum-1vsrest-df4-ratio-normalization',
'Rhla_sum-3vsrest-df1-ratio-normalization' : 'Rhla_sum-3vsrest-df1-ratio-normalization',
'Rhla_sum5a-2vsrest-df5-log-normalization' : 'Rhla_sum5a-2vsrest-df5-log-normalization',
'Rhla_sum-3vsrest-df2-ratio-normalization' : 'Rhla_sum-3vsrest-df2-ratio-normalization',
'Rhla_sum-3vsrest-df1-log' : 'Rhla_sum-3vsrest-df1-log',
'Rhla_5a-3vsrest-df5-log-normalization' : 'Rhla_5a-3vsrest-df5-log-normalization',
'Rhla_sum5a-3vsrest-df1-ratio-normalization' : 'Rhla_sum5a-3vsrest-df1-ratio-normalization',
'Rhla_sum-0vsrest-df3-ratio' : 'Rhla_sum-0vsrest-df3-ratio',
'Rhla_sum5a-3vsrest-df3-log' : 'Rhla_sum5a-3vsrest-df3-log',
'Rhla_sum-0vsrest-df1-log' : 'Rhla_sum-0vsrest-df1-log',
'Rhla_sum-1vsrest-df3-log-normalization' : 'Rhla_sum-1vsrest-df3-log-normalization',
'Rhla_sum-3vsrest-df5-ratio' : 'Rhla_sum-3vsrest-df5-ratio',
'Rhla_sum-1vsrest-df3-ratio-normalization' : 'Rhla_sum-1vsrest-df3-ratio-normalization',
'Rhla_sum-1vsrest-df4-ratio' : 'Rhla_sum-1vsrest-df4-ratio',
'Rhla_sum5a-0vsrest-df4-log' : 'Rhla_sum5a-0vsrest-df4-log',
'Rhla_5a-3vsrest-df4-log-normalization' : 'Rhla_5a-3vsrest-df4-log-normalization',
'Rhla_sum-3vsrest-df5-log-normalization' : 'Rhla_sum-3vsrest-df5-log-normalization',
'Rhla_sum5a-1vsrest-df3-ratio-normalization' : 'Rhla_sum5a-1vsrest-df3-ratio-normalization',
'Rhla_5a-3vsrest-df3-ratio' : 'Rhla_5a-3vsrest-df3-ratio',
'Rhla_sum-3vsrest-df2-ratio' : 'Rhla_sum-3vsrest-df2-ratio',
'Rhla_5a-0vsrest-df5-ratio-normalization' : 'Rhla_5a-0vsrest-df5-ratio-normalization',
'Rhla_sum-0vsrest-df3-log' : 'Rhla_sum-0vsrest-df3-log',
'Rhla_sum-0vsrest-df5-ratio' : 'Rhla_sum-0vsrest-df5-ratio',
'Rhla_5a-3vsrest-df3-log-normalization' : 'Rhla_5a-3vsrest-df3-log-normalization',
'Rhla_sum5a-1vsrest-df1-log-normalization' : 'Rhla_sum5a-1vsrest-df1-log-normalization',
'Rhla_sum5a-0vsrest-df3-ratio' : 'Rhla_sum5a-0vsrest-df3-ratio',
'Rhla_sum-3vsrest-df5-ratio-normalization' : 'Rhla_sum-3vsrest-df5-ratio-normalization',
'Rhla_sum5a-1vsrest-df5-ratio' : 'Rhla_sum5a-1vsrest-df5-ratio',
'Rhla_sum5a-1vsrest-df3-log' : 'Rhla_sum5a-1vsrest-df3-log',
'Rhla_sum5a-0vsrest-df3-ratio-normalization' : 'Rhla_sum5a-0vsrest-df3-ratio-normalization',
'Rhla_sum-0vsrest-df4-ratio' : 'Rhla_sum-0vsrest-df4-ratio',
'Rhla_5a-2vsrest-df2-log-normalization' : 'Rhla_5a-2vsrest-df2-log-normalization',
'Rhla_sum5a-3vsrest-df3-ratio' : 'Rhla_sum5a-3vsrest-df3-ratio',
'Rhla_sum-1vsrest-df5-log' : 'Rhla_sum-1vsrest-df5-log',
'Rhla_sum-1vsrest-df5-ratio' : 'Rhla_sum-1vsrest-df5-ratio',
'Rhla_sum-2vsrest-df5-log' : 'Rhla_sum-2vsrest-df5-log',
'Rhla_sum-3vsrest-df3-ratio-normalization' : 'Rhla_sum-3vsrest-df3-ratio-normalization',
'Rhla_sum5a-2vsrest-df4-log-normalization' : 'Rhla_sum5a-2vsrest-df4-log-normalization',
'Rhla_sum5a-0vsrest-df2-ratio' : 'Rhla_sum5a-0vsrest-df2-ratio',
'Rhla_5a-1vsrest-df1-log' : 'Rhla_5a-1vsrest-df1-log',
'Rhla_sum5a-2vsrest-df3-log-normalization' : 'Rhla_sum5a-2vsrest-df3-log-normalization',
'Rhla_sum5a-2vsrest-df2-log-normalization' : 'Rhla_sum5a-2vsrest-df2-log-normalization',
'Rhla_sum-1vsrest-df2-ratio-normalization' : 'Rhla_sum-1vsrest-df2-ratio-normalization',
'Rhla_sum5a-0vsrest-df1-ratio-normalization' : 'Rhla_sum5a-0vsrest-df1-ratio-normalization',
'Rhla_sum5a-0vsrest-df4-ratio' : 'Rhla_sum5a-0vsrest-df4-ratio',
'Rhla_sum5a-2vsrest-df1-ratio-normalization' : 'Rhla_sum5a-2vsrest-df1-ratio-normalization',
'Rhla_sum5a-1vsrest-df1-ratio' : 'Rhla_sum5a-1vsrest-df1-ratio',
'Rhla_sum-2vsrest-df2-ratio-normalization' : 'Rhla_sum-2vsrest-df2-ratio-normalization',
'Rhla_sum5a-0vsrest-df5-log-normalization' : 'Rhla_sum5a-0vsrest-df5-log-normalization',
'Rhla_sum5a-1vsrest-df2-ratio-normalization' : 'Rhla_sum5a-1vsrest-df2-ratio-normalization',
'Rhla_sum5a-0vsrest-df5-ratio' : 'Rhla_sum5a-0vsrest-df5-ratio',
'Rhla_5a-1vsrest-df4-log' : 'Rhla_5a-1vsrest-df4-log',
'Rhla_sum-1vsrest-df1-log' : 'Rhla_sum-1vsrest-df1-log',
'Rhla_5a-0vsrest-df3-log' : 'Rhla_5a-0vsrest-df3-log',
'Rhla_5a-1vsrest-df5-ratio' : 'Rhla_5a-1vsrest-df5-ratio',
'Rhla_sum5a-3vsrest-df4-ratio-normalization' : 'Rhla_sum5a-3vsrest-df4-ratio-normalization',
'Rhla_sum-3vsrest-df4-log-normalization' : 'Rhla_sum-3vsrest-df4-log-normalization',
'Rhla_5a-2vsrest-df2-ratio' : 'Rhla_5a-2vsrest-df2-ratio',
'Rhla_sum5a-2vsrest-df1-log' : 'Rhla_sum5a-2vsrest-df1-log',
'Rhla_sum5a-0vsrest-df2-log' : 'Rhla_sum5a-0vsrest-df2-log',
'Rhla_5a-0vsrest-df5-ratio' : 'Rhla_5a-0vsrest-df5-ratio',
'Rhla_5a-2vsrest-df4-log-normalization' : 'Rhla_5a-2vsrest-df4-log-normalization',
'Rhla_sum-1vsrest-df3-ratio' : 'Rhla_sum-1vsrest-df3-ratio',
'Rhla_sum-1vsrest-df5-log-normalization' : 'Rhla_sum-1vsrest-df5-log-normalization',
'Rhla_sum5a-0vsrest-df5-log' : 'Rhla_sum5a-0vsrest-df5-log',
'Rhla_5a-2vsrest-df3-log-normalization' : 'Rhla_5a-2vsrest-df3-log-normalization',
'Rhla_sum5a-3vsrest-df1-log-normalization' : 'Rhla_sum5a-3vsrest-df1-log-normalization',
'Rhla_5a-0vsrest-df3-log-normalization' : 'Rhla_5a-0vsrest-df3-log-normalization',
'Rhla_5a-0vsrest-df1-log' : 'Rhla_5a-0vsrest-df1-log',
'Rhla_5a-1vsrest-df5-ratio-normalization' : 'Rhla_5a-1vsrest-df5-ratio-normalization',
'Rhla_5a-1vsrest-df1-ratio-normalization' : 'Rhla_5a-1vsrest-df1-ratio-normalization',
'Rhla_5a-3vsrest-df3-log' : 'Rhla_5a-3vsrest-df3-log',
'Rhla_sum5a-3vsrest-df5-ratio' : 'Rhla_sum5a-3vsrest-df5-ratio',
'Rhla_sum-0vsrest-df2-ratio-normalization' : 'Rhla_sum-0vsrest-df2-ratio-normalization',
'Rhla_sum-0vsrest-df1-log-normalization' : 'Rhla_sum-0vsrest-df1-log-normalization',
'Rhla_sum5a-1vsrest-df5-log' : 'Rhla_sum5a-1vsrest-df5-log',
'Rhla_sum5a-0vsrest-df5-ratio-normalization' : 'Rhla_sum5a-0vsrest-df5-ratio-normalization',
'Rhla_sum5a-2vsrest-df4-ratio-normalization' : 'Rhla_sum5a-2vsrest-df4-ratio-normalization',
'Rhla_5a-1vsrest-df3-log-normalization' : 'Rhla_5a-1vsrest-df3-log-normalization',
'Rhla_sum5a-1vsrest-df1-ratio-normalization' : 'Rhla_sum5a-1vsrest-df1-ratio-normalization',
'Rhla_5a-0vsrest-df5-log-normalization' : 'Rhla_5a-0vsrest-df5-log-normalization',
'Rhla_5a-0vsrest-df2-log-normalization' : 'Rhla_5a-0vsrest-df2-log-normalization',
'Rhla_sum5a-0vsrest-df2-ratio-normalization' : 'Rhla_sum5a-0vsrest-df2-ratio-normalization',
'Rhla_sum-0vsrest-df5-log-normalization' : 'Rhla_sum-0vsrest-df5-log-normalization',
'Rhla_5a-1vsrest-df3-ratio' : 'Rhla_5a-1vsrest-df3-ratio',
'Rhla_sum-3vsrest-df3-log' : 'Rhla_sum-3vsrest-df3-log',
'Rhla_sum-1vsrest-df3-log' : 'Rhla_sum-1vsrest-df3-log',
'Rhla_sum-2vsrest-df1-log' : 'Rhla_sum-2vsrest-df1-log',
'Rhla_5a-0vsrest-df1-log-normalization' : 'Rhla_5a-0vsrest-df1-log-normalization',
'Rhla_sum-0vsrest-df3-log-normalization' : 'Rhla_sum-0vsrest-df3-log-normalization',
'Rhla_sum5a-0vsrest-df2-log-normalization' : 'Rhla_sum5a-0vsrest-df2-log-normalization',
'Rhla_5a-3vsrest-df1-log' : 'Rhla_5a-3vsrest-df1-log',
'Rhla_5a-2vsrest-df3-log' : 'Rhla_5a-2vsrest-df3-log',
'Rhla_sum5a-1vsrest-df4-log' : 'Rhla_sum5a-1vsrest-df4-log',
'Rhla_sum-3vsrest-df1-ratio' : 'Rhla_sum-3vsrest-df1-ratio',
'Rhla_sum5a-1vsrest-df3-ratio' : 'Rhla_sum5a-1vsrest-df3-ratio',
'Rhla_5a-2vsrest-df5-ratio' : 'Rhla_5a-2vsrest-df5-ratio',
'Rhla_5a-3vsrest-df1-ratio' : 'Rhla_5a-3vsrest-df1-ratio',
'Rhla_sum-2vsrest-df3-log' : 'Rhla_sum-2vsrest-df3-log',
'Rhla_5a-1vsrest-df5-log-normalization' : 'Rhla_5a-1vsrest-df5-log-normalization',
'Rhla_5a-3vsrest-df5-ratio-normalization' : 'Rhla_5a-3vsrest-df5-ratio-normalization',
'Rhla_5a-3vsrest-df2-log-normalization' : 'Rhla_5a-3vsrest-df2-log-normalization',
'Rhla_sum5a-3vsrest-df3-ratio-normalization' : 'Rhla_sum5a-3vsrest-df3-ratio-normalization',
'Rhla_sum-2vsrest-df4-log' : 'Rhla_sum-2vsrest-df4-log',
'Rhla_5a-1vsrest-df1-log-normalization' : 'Rhla_5a-1vsrest-df1-log-normalization',
'Rhla_sum-2vsrest-df1-ratio-normalization' : 'Rhla_sum-2vsrest-df1-ratio-normalization',
'Rhla_sum-0vsrest-df1-ratio-normalization' : 'Rhla_sum-0vsrest-df1-ratio-normalization',
'Rhla_sum-3vsrest-df2-log' : 'Rhla_sum-3vsrest-df2-log',
'Rhla_sum-2vsrest-df1-log-normalization' : 'Rhla_sum-2vsrest-df1-log-normalization',
'Rhla_sum5a-2vsrest-df3-ratio-normalization' : 'Rhla_sum5a-2vsrest-df3-ratio-normalization',
'Rhla_5a-3vsrest-df4-ratio-normalization' : 'Rhla_5a-3vsrest-df4-ratio-normalization',
'Rhla_sum5a-0vsrest-df1-log' : 'Rhla_sum5a-0vsrest-df1-log',
'Rhla_5a-3vsrest-df1-ratio-normalization' : 'Rhla_5a-3vsrest-df1-ratio-normalization',
'Rhla_sum5a-1vsrest-df2-ratio' : 'Rhla_sum5a-1vsrest-df2-ratio',
'Rhla_sum-2vsrest-df2-log' : 'Rhla_sum-2vsrest-df2-log',
'Rhla_sum-1vsrest-df4-log-normalization' : 'Rhla_sum-1vsrest-df4-log-normalization',
'Rhla_sum5a-2vsrest-df4-log' : 'Rhla_sum5a-2vsrest-df4-log',
'Rhla_sum-1vsrest-df1-ratio-normalization' : 'Rhla_sum-1vsrest-df1-ratio-normalization',
'Rhla_5a-1vsrest-df3-ratio-normalization' : 'Rhla_5a-1vsrest-df3-ratio-normalization',
'Rhla_5a-2vsrest-df3-ratio' : 'Rhla_5a-2vsrest-df3-ratio',
'Rhla_sum5a-3vsrest-df5-log-normalization' : 'Rhla_sum5a-3vsrest-df5-log-normalization',
'Rhla_sum5a-1vsrest-df5-ratio-normalization' : 'Rhla_sum5a-1vsrest-df5-ratio-normalization',
'Rhla_sum5a-3vsrest-df4-log-normalization' : 'Rhla_sum5a-3vsrest-df4-log-normalization',
'Rhla_5a-2vsrest-df2-log' : 'Rhla_5a-2vsrest-df2-log',
'Rhla_sum5a-3vsrest-df4-ratio' : 'Rhla_sum5a-3vsrest-df4-ratio',
'Rhla_sum5a-2vsrest-df2-log' : 'Rhla_sum5a-2vsrest-df2-log',
'Rhla_sum-0vsrest-df5-ratio-normalization' : 'Rhla_sum-0vsrest-df5-ratio-normalization',
'Rhla_5a-1vsrest-df4-ratio' : 'Rhla_5a-1vsrest-df4-ratio',
'Rhla_5a-2vsrest-df2-ratio-normalization' : 'Rhla_5a-2vsrest-df2-ratio-normalization',
'Rhla_sum-3vsrest-df4-ratio-normalization' : 'Rhla_sum-3vsrest-df4-ratio-normalization',
'Rhla_sum-1vsrest-df5-ratio-normalization' : 'Rhla_sum-1vsrest-df5-ratio-normalization',
'Rhla_sum5a-2vsrest-df4-ratio' : 'Rhla_sum5a-2vsrest-df4-ratio',
'Rhla_5a-1vsrest-df2-ratio-normalization' : 'Rhla_5a-1vsrest-df2-ratio-normalization',
'Rhla_5a-0vsrest-df4-ratio' : 'Rhla_5a-0vsrest-df4-ratio',
'Rhla_sum5a-2vsrest-df2-ratio' : 'Rhla_sum5a-2vsrest-df2-ratio',
'Rhla_sum-2vsrest-df1-ratio' : 'Rhla_sum-2vsrest-df1-ratio',
'Rhla_sum5a-0vsrest-df4-ratio-normalization' : 'Rhla_sum5a-0vsrest-df4-ratio-normalization',
'Rhla_5a-2vsrest-df1-log' : 'Rhla_5a-2vsrest-df1-log',
'Rhla_sum5a-2vsrest-df2-ratio-normalization' : 'Rhla_sum5a-2vsrest-df2-ratio-normalization',
'Rhla_sum5a-0vsrest-df1-ratio' : 'Rhla_sum5a-0vsrest-df1-ratio',
'Rhla_5a-0vsrest-df4-log' : 'Rhla_5a-0vsrest-df4-log',
'Rhla_sum-3vsrest-df3-ratio' : 'Rhla_sum-3vsrest-df3-ratio',
'Rhla_sum-0vsrest-df2-log' : 'Rhla_sum-0vsrest-df2-log',
'Rhla_sum-1vsrest-df1-ratio' : 'Rhla_sum-1vsrest-df1-ratio',
'Rhla_5a-2vsrest-df4-ratio' : 'Rhla_5a-2vsrest-df4-ratio',
'Rhla_sum5a-1vsrest-df2-log' : 'Rhla_sum5a-1vsrest-df2-log',
'Rhla_sum5a-2vsrest-df1-log-normalization' : 'Rhla_sum5a-2vsrest-df1-log-normalization',
'Rhla_sum-2vsrest-df5-ratio-normalization' : 'Rhla_sum-2vsrest-df5-ratio-normalization',
'Rhla_sum5a-1vsrest-df4-ratio' : 'Rhla_sum5a-1vsrest-df4-ratio',
'Rhla_5a-3vsrest-df5-log' : 'Rhla_5a-3vsrest-df5-log',
'Rhla_sum-3vsrest-df5-log' : 'Rhla_sum-3vsrest-df5-log',


'Rhla_sum-3vsrest-df4' : 'Rhla_sum-3vsrest-df4',
'Rhla_5a-3vsrest-df2' : 'Rhla_5a-3vsrest-df2',
'Rhla_sum5a-3vsrest-df1' : 'Rhla_sum5a-3vsrest-df1',
'Rhla_5a-3vsrest-df5' : 'Rhla_5a-3vsrest-df5',
'Rhla_sum-3vsrest-df2' : 'Rhla_sum-3vsrest-df2',
'Rhla_sum-3vsrest-df1' : 'Rhla_sum-3vsrest-df1',
'Rhla_5a-3vsrest-df3' : 'Rhla_5a-3vsrest-df3',
'Rhla_sum5a-3vsrest-df4' : 'Rhla_sum5a-3vsrest-df4',
'Rhla_sum5a-3vsrest-df5' : 'Rhla_sum5a-3vsrest-df5',
'Rhla_sum-3vsrest-df5' : 'Rhla_sum-3vsrest-df5',
'Rhla_5a-3vsrest-df4' : 'Rhla_5a-3vsrest-df4',
'Rhla_sum5a-3vsrest-df3' : 'Rhla_sum5a-3vsrest-df3',
'Rhla_sum-3vsrest-df3' : 'Rhla_sum-3vsrest-df3',
'Rhla_5a-3vsrest-df1' : 'Rhla_5a-3vsrest-df1',
'Rhla_sum5a-3vsrest-df2' : 'Rhla_sum5a-3vsrest-df2',

'CR6261_h9-0vsrest-df1' : 'CR6261_h9-0vsrest-df1',
'CR6261_h1-1vsrest-df3' : 'CR6261_h1-1vsrest-df3',
'CR6261_h9-2vsrest-df4' : 'CR6261_h9-2vsrest-df4',
'CR6261_h1-1vsrest-df5' : 'CR6261_h1-1vsrest-df5',
'CR6261_h1-2vsrest-df4' : 'CR6261_h1-2vsrest-df4',
'CR6261_h9-3vsrest-df2' : 'CR6261_h9-3vsrest-df2',
'CR6261_h1-1vsrest-df1' : 'CR6261_h1-1vsrest-df1',
'CR6261_h1-2vsrest-df1' : 'CR6261_h1-2vsrest-df1',
'CR6261_h9-1vsrest-df2' : 'CR6261_h9-1vsrest-df2',
'CR6261_h9-1vsrest-df3' : 'CR6261_h9-1vsrest-df3',
'CR6261_h1-3vsrest-df3' : 'CR6261_h1-3vsrest-df3',
'CR6261_h1-1vsrest-df2' : 'CR6261_h1-1vsrest-df2',
'CR6261_h1-0vsrest-df3' : 'CR6261_h1-0vsrest-df3',
'CR6261_h1-3vsrest-df5' : 'CR6261_h1-3vsrest-df5',
'CR6261_h1-3vsrest-df1' : 'CR6261_h1-3vsrest-df1',
'CR6261_h9-0vsrest-df2' : 'CR6261_h9-0vsrest-df2',
'CR6261_h1-0vsrest-df5' : 'CR6261_h1-0vsrest-df5',
'CR6261_h1-2vsrest-df2' : 'CR6261_h1-2vsrest-df2',
'CR6261_h9-0vsrest-df3' : 'CR6261_h9-0vsrest-df3',
'CR6261_h9-2vsrest-df2' : 'CR6261_h9-2vsrest-df2',
'CR6261_h1-0vsrest-df2' : 'CR6261_h1-0vsrest-df2',
'CR6261_h9-2vsrest-df3' : 'CR6261_h9-2vsrest-df3',
'CR6261_h9-1vsrest-df4' : 'CR6261_h9-1vsrest-df4',
'CR6261_h1-1vsrest-df4' : 'CR6261_h1-1vsrest-df4',
'CR6261_h1-3vsrest-df4' : 'CR6261_h1-3vsrest-df4',
'CR6261_h9-3vsrest-df3' : 'CR6261_h9-3vsrest-df3',
'CR6261_h9-3vsrest-df5' : 'CR6261_h9-3vsrest-df5',
'CR6261_h9-1vsrest-df1' : 'CR6261_h9-1vsrest-df1',
'CR6261_h9-0vsrest-df4' : 'CR6261_h9-0vsrest-df4',
'CR6261_h9-2vsrest-df5' : 'CR6261_h9-2vsrest-df5',
'CR6261_h1-3vsrest-df2' : 'CR6261_h1-3vsrest-df2',
'CR6261_h9-0vsrest-df5' : 'CR6261_h9-0vsrest-df5',
'CR6261_h9-3vsrest-df1' : 'CR6261_h9-3vsrest-df1',
'CR6261_h9-2vsrest-df1' : 'CR6261_h9-2vsrest-df1',
'CR6261_h9-1vsrest-df5' : 'CR6261_h9-1vsrest-df5',
'CR6261_h1-2vsrest-df5' : 'CR6261_h1-2vsrest-df5',
'CR6261_h1-0vsrest-df4' : 'CR6261_h1-0vsrest-df4',
'CR6261_h1-2vsrest-df3' : 'CR6261_h1-2vsrest-df3',
'CR6261_h9-3vsrest-df4' : 'CR6261_h9-3vsrest-df4',
'CR6261_h1-0vsrest-df1' : 'CR6261_h1-0vsrest-df1',


'CR9114_h1-3vsrest-df5' : 'CR9114_h1-3vsrest-df5',
'CR9114_h1-3vsrest-df4' : 'CR9114_h1-3vsrest-df4',
'CR9114_h1-0vsrest-df3' : 'CR9114_h1-0vsrest-df3',
'CR9114_h1-2vsrest-df1' : 'CR9114_h1-2vsrest-df1',
'CR9114_h1-0vsrest-df5' : 'CR9114_h1-0vsrest-df5',
'CR9114_h1-1vsrest-df4' : 'CR9114_h1-1vsrest-df4',
'CR9114_h1-2vsrest-df3' : 'CR9114_h1-2vsrest-df3',
'CR9114_h1-2vsrest-df2' : 'CR9114_h1-2vsrest-df2',
'CR9114_h1-2vsrest-df5' : 'CR9114_h1-2vsrest-df5',
'CR9114_h1-3vsrest-df1' : 'CR9114_h1-3vsrest-df1',
'CR9114_h1-2vsrest-df4' : 'CR9114_h1-2vsrest-df4',
'CR9114_h1-1vsrest-df3' : 'CR9114_h1-1vsrest-df3',
'CR9114_h1-3vsrest-df2' : 'CR9114_h1-3vsrest-df2',
'CR9114_h1-3vsrest-df3' : 'CR9114_h1-3vsrest-df3',
'CR9114_h1-0vsrest-df4' : 'CR9114_h1-0vsrest-df4',
'CR9114_h1-0vsrest-df2' : 'CR9114_h1-0vsrest-df2',
'CR9114_h1-1vsrest-df2' : 'CR9114_h1-1vsrest-df2',
'CR9114_h1-0vsrest-df1' : 'CR9114_h1-0vsrest-df1',
'CR9114_h1-1vsrest-df5' : 'CR9114_h1-1vsrest-df5',
'CR9114_h1-1vsrest-df1' : 'CR9114_h1-1vsrest-df1',

'SaCas9_mean-0vsrest-df1' : 'SaCas9_mean-0vsrest-df1',
'SaCas9_mean-2vsrest-df4' : 'SaCas9_mean-2vsrest-df4',
'SaCas9_mean-3vsrest-df1' : 'SaCas9_mean-3vsrest-df1',
'SaCas9_mean-1vsrest-df5' : 'SaCas9_mean-1vsrest-df5',
'SaCas9_mean-0vsrest-df2' : 'SaCas9_mean-0vsrest-df2',
'SaCas9_mean-2vsrest-df3' : 'SaCas9_mean-2vsrest-df3',
'SaCas9_mean-0vsrest-df3' : 'SaCas9_mean-0vsrest-df3',
'SaCas9_mean-2vsrest-df5' : 'SaCas9_mean-2vsrest-df5',
'SaCas9_mean-3vsrest-df3' : 'SaCas9_mean-3vsrest-df3',
'SaCas9_mean-2vsrest-df2' : 'SaCas9_mean-2vsrest-df2',
'SaCas9_mean-3vsrest-df2' : 'SaCas9_mean-3vsrest-df2',
'SaCas9_mean-3vsrest-df4' : 'SaCas9_mean-3vsrest-df4',
'SaCas9_mean-1vsrest-df1' : 'SaCas9_mean-1vsrest-df1',
'SaCas9_mean-0vsrest-df4' : 'SaCas9_mean-0vsrest-df4',
'SaCas9_mean-3vsrest-df5' : 'SaCas9_mean-3vsrest-df5',
'SaCas9_mean-2vsrest-df1' : 'SaCas9_mean-2vsrest-df1',
'SaCas9_mean-1vsrest-df2' : 'SaCas9_mean-1vsrest-df2',
'SaCas9_mean-0vsrest-df5' : 'SaCas9_mean-0vsrest-df5',
'SaCas9_mean-1vsrest-df4' : 'SaCas9_mean-1vsrest-df4',
'SaCas9_mean-1vsrest-df3' : 'SaCas9_mean-1vsrest-df3',

'SpCas9_mean-2vsrest-df4' : 'SpCas9_mean-2vsrest-df4',
'SpCas9_mean-1vsrest-df1' : 'SpCas9_mean-1vsrest-df1',
'SpCas9_mean-3vsrest-df1' : 'SpCas9_mean-3vsrest-df1',
'SpCas9_mean-3vsrest-df5' : 'SpCas9_mean-3vsrest-df5',
'SpCas9_mean-3vsrest-df3' : 'SpCas9_mean-3vsrest-df3',
'SpCas9_mean-3vsrest-df4' : 'SpCas9_mean-3vsrest-df4',
'SpCas9_mean-1vsrest-df5' : 'SpCas9_mean-1vsrest-df5',
'SpCas9_mean-1vsrest-df3' : 'SpCas9_mean-1vsrest-df3',
'SpCas9_mean-2vsrest-df1' : 'SpCas9_mean-2vsrest-df1',
'SpCas9_mean-0vsrest-df1' : 'SpCas9_mean-0vsrest-df1',
'SpCas9_mean-1vsrest-df2' : 'SpCas9_mean-1vsrest-df2',
'SpCas9_mean-1vsrest-df4' : 'SpCas9_mean-1vsrest-df4',
'SpCas9_mean-0vsrest-df2' : 'SpCas9_mean-0vsrest-df2',
'SpCas9_mean-0vsrest-df5' : 'SpCas9_mean-0vsrest-df5',
'SpCas9_mean-3vsrest-df2' : 'SpCas9_mean-3vsrest-df2',
'SpCas9_mean-2vsrest-df2' : 'SpCas9_mean-2vsrest-df2',
'SpCas9_mean-2vsrest-df5' : 'SpCas9_mean-2vsrest-df5',
'SpCas9_mean-0vsrest-df4' : 'SpCas9_mean-0vsrest-df4',
'SpCas9_mean-2vsrest-df3' : 'SpCas9_mean-2vsrest-df3',
'SpCas9_mean-0vsrest-df3' : 'SpCas9_mean-0vsrest-df3',


'eqFP611_blue-0vsrest-df3' : 'eqFP611_blue-0vsrest-df3',
'eqFP611_combined-0vsrest-df1' : 'eqFP611_combined-0vsrest-df1',
'eqFP611_red-2vsrest-df1' : 'eqFP611_red-2vsrest-df1',
'eqFP611_combined-2vsrest-df1' : 'eqFP611_combined-2vsrest-df1',
'eqFP611_red-2vsrest-df4' : 'eqFP611_red-2vsrest-df4',
'eqFP611_red-1vsrest-df3' : 'eqFP611_red-1vsrest-df3',
'eqFP611_red-1vsrest-df1' : 'eqFP611_red-1vsrest-df1',
'eqFP611_combined-1vsrest-df2' : 'eqFP611_combined-1vsrest-df2',
'eqFP611_blue-3vsrest-df5' : 'eqFP611_blue-3vsrest-df5',
'eqFP611_red-3vsrest-df1' : 'eqFP611_red-3vsrest-df1',
'eqFP611_blue-2vsrest-df1' : 'eqFP611_blue-2vsrest-df1',
'eqFP611_combined-3vsrest-df4' : 'eqFP611_combined-3vsrest-df4',
'eqFP611_red-3vsrest-df5' : 'eqFP611_red-3vsrest-df5',
'eqFP611_red-0vsrest-df4' : 'eqFP611_red-0vsrest-df4',
'eqFP611_blue-2vsrest-df3' : 'eqFP611_blue-2vsrest-df3',
'eqFP611_blue-0vsrest-df4' : 'eqFP611_blue-0vsrest-df4',
'eqFP611_combined-3vsrest-df2' : 'eqFP611_combined-3vsrest-df2',
'eqFP611_blue-1vsrest-df1' : 'eqFP611_blue-1vsrest-df1',
'eqFP611_blue-1vsrest-df2' : 'eqFP611_blue-1vsrest-df2',
'eqFP611_blue-0vsrest-df2' : 'eqFP611_blue-0vsrest-df2',
'eqFP611_combined-0vsrest-df3' : 'eqFP611_combined-0vsrest-df3',
'eqFP611_red-1vsrest-df4' : 'eqFP611_red-1vsrest-df4',
'eqFP611_red-2vsrest-df5' : 'eqFP611_red-2vsrest-df5',
'eqFP611_red-0vsrest-df2' : 'eqFP611_red-0vsrest-df2',
'eqFP611_blue-3vsrest-df1' : 'eqFP611_blue-3vsrest-df1',
'eqFP611_combined-3vsrest-df5' : 'eqFP611_combined-3vsrest-df5',
'eqFP611_combined-2vsrest-df3' : 'eqFP611_combined-2vsrest-df3',
'eqFP611_red-3vsrest-df4' : 'eqFP611_red-3vsrest-df4',
'eqFP611_combined-0vsrest-df5' : 'eqFP611_combined-0vsrest-df5',
'eqFP611_red-3vsrest-df2' : 'eqFP611_red-3vsrest-df2',
'eqFP611_red-0vsrest-df1' : 'eqFP611_red-0vsrest-df1',
'eqFP611_blue-0vsrest-df5' : 'eqFP611_blue-0vsrest-df5',
'eqFP611_blue-2vsrest-df2' : 'eqFP611_blue-2vsrest-df2',
'eqFP611_combined-2vsrest-df2' : 'eqFP611_combined-2vsrest-df2',
'eqFP611_combined-2vsrest-df5' : 'eqFP611_combined-2vsrest-df5',
'eqFP611_blue-1vsrest-df4' : 'eqFP611_blue-1vsrest-df4',
'eqFP611_combined-1vsrest-df3' : 'eqFP611_combined-1vsrest-df3',
'eqFP611_combined-2vsrest-df4' : 'eqFP611_combined-2vsrest-df4',
'eqFP611_blue-1vsrest-df3' : 'eqFP611_blue-1vsrest-df3',
'eqFP611_blue-3vsrest-df3' : 'eqFP611_blue-3vsrest-df3',
'eqFP611_red-1vsrest-df5' : 'eqFP611_red-1vsrest-df5',
'eqFP611_combined-0vsrest-df2' : 'eqFP611_combined-0vsrest-df2',
'eqFP611_red-0vsrest-df5' : 'eqFP611_red-0vsrest-df5',
'eqFP611_blue-0vsrest-df1' : 'eqFP611_blue-0vsrest-df1',
'eqFP611_red-2vsrest-df3' : 'eqFP611_red-2vsrest-df3',
'eqFP611_blue-2vsrest-df4' : 'eqFP611_blue-2vsrest-df4',
'eqFP611_red-0vsrest-df3' : 'eqFP611_red-0vsrest-df3',
'eqFP611_blue-1vsrest-df5' : 'eqFP611_blue-1vsrest-df5',
'eqFP611_blue-3vsrest-df2' : 'eqFP611_blue-3vsrest-df2',
'eqFP611_red-3vsrest-df3' : 'eqFP611_red-3vsrest-df3',
'eqFP611_red-2vsrest-df2' : 'eqFP611_red-2vsrest-df2',
'eqFP611_combined-0vsrest-df4' : 'eqFP611_combined-0vsrest-df4',
'eqFP611_combined-1vsrest-df1' : 'eqFP611_combined-1vsrest-df1',
'eqFP611_blue-3vsrest-df4' : 'eqFP611_blue-3vsrest-df4',
'eqFP611_blue-2vsrest-df5' : 'eqFP611_blue-2vsrest-df5',
'eqFP611_combined-1vsrest-df5' : 'eqFP611_combined-1vsrest-df5',
'eqFP611_combined-3vsrest-df3' : 'eqFP611_combined-3vsrest-df3',
'eqFP611_red-1vsrest-df2' : 'eqFP611_red-1vsrest-df2',
'eqFP611_combined-1vsrest-df4' : 'eqFP611_combined-1vsrest-df4',
'eqFP611_combined-3vsrest-df1' : 'eqFP611_combined-3vsrest-df1',

'HIV_1-2vsrest-df4' : 'HIV_1-2vsrest-df4',
'HIV_1-1vsrest-df3' : 'HIV_1-1vsrest-df3',
'HIV_1-0vsrest-df3' : 'HIV_1-0vsrest-df3',
'HIV_1-0vsrest-df1' : 'HIV_1-0vsrest-df1',
'HIV_1-3vsrest-df1' : 'HIV_1-3vsrest-df1',
'HIV_1-1vsrest-df2' : 'HIV_1-1vsrest-df2',
'HIV_1-3vsrest-df2' : 'HIV_1-3vsrest-df2',
'HIV_1-3vsrest-df3' : 'HIV_1-3vsrest-df3',
'HIV_1-2vsrest-df5' : 'HIV_1-2vsrest-df5',
'HIV_1-0vsrest-df2' : 'HIV_1-0vsrest-df2',
'HIV_1-3vsrest-df4' : 'HIV_1-3vsrest-df4',
'HIV_1-2vsrest-df3' : 'HIV_1-2vsrest-df3',
'HIV_1-1vsrest-df5' : 'HIV_1-1vsrest-df5',
'HIV_1-2vsrest-df2' : 'HIV_1-2vsrest-df2',
'HIV_1-3vsrest-df5' : 'HIV_1-3vsrest-df5',
'HIV_1-0vsrest-df5' : 'HIV_1-0vsrest-df5',
'HIV_1-2vsrest-df1' : 'HIV_1-2vsrest-df1',
'HIV_1-1vsrest-df4' : 'HIV_1-1vsrest-df4',
'HIV_1-1vsrest-df1' : 'HIV_1-1vsrest-df1',
'HIV_1-0vsrest-df4' : 'HIV_1-0vsrest-df4',

'gb1_sample-2vsrest-df4' : 'gb1_sample-2vsrest-df4',
'gb1_sample-3vsrest-df3' : 'gb1_sample-3vsrest-df3',
'gb1_sample-2vsrest-df2' : 'gb1_sample-2vsrest-df2',
'gb1_sample-1vsrest-df3' : 'gb1_sample-1vsrest-df3',
'gb1_sample-1vsrest-df2' : 'gb1_sample-1vsrest-df2',
'gb1_sample-1vsrest-df5' : 'gb1_sample-1vsrest-df5',
'gb1_sample-0vsrest-df1' : 'gb1_sample-0vsrest-df1',
'gb1_sample-1vsrest-df4' : 'gb1_sample-1vsrest-df4',
'gb1_sample-2vsrest-df5' : 'gb1_sample-2vsrest-df5',
'gb1_sample-0vsrest-df3' : 'gb1_sample-0vsrest-df3',
'gb1_sample-0vsrest-df4' : 'gb1_sample-0vsrest-df4',
'gb1_sample-3vsrest-df4' : 'gb1_sample-3vsrest-df4',
'gb1_sample-2vsrest-df1' : 'gb1_sample-2vsrest-df1',
'gb1_sample-3vsrest-df1' : 'gb1_sample-3vsrest-df1',
'gb1_sample-0vsrest-df2' : 'gb1_sample-0vsrest-df2',
'gb1_sample-2vsrest-df3' : 'gb1_sample-2vsrest-df3',
'gb1_sample-3vsrest-df2' : 'gb1_sample-3vsrest-df2',
'gb1_sample-1vsrest-df1' : 'gb1_sample-1vsrest-df1',
'gb1_sample-3vsrest-df5' : 'gb1_sample-3vsrest-df5',
'gb1_sample-0vsrest-df5' : 'gb1_sample-0vsrest-df5',



'CR9114_h1sample-1vsrest-df4' : 'CR9114_h1sample-1vsrest-df4',
'CR9114_h1sample-0vsrest-df5' : 'CR9114_h1sample-0vsrest-df5',
'CR9114_h1sample-0vsrest-df3' : 'CR9114_h1sample-0vsrest-df3',
'CR9114_h1sample-2vsrest-df2' : 'CR9114_h1sample-2vsrest-df2',
'CR9114_h1sample-3vsrest-df5' : 'CR9114_h1sample-3vsrest-df5',
'CR9114_h1sample-3vsrest-df2' : 'CR9114_h1sample-3vsrest-df2',
'CR9114_h1sample-2vsrest-df3' : 'CR9114_h1sample-2vsrest-df3',
'CR9114_h1sample-3vsrest-df1' : 'CR9114_h1sample-3vsrest-df1',
'CR9114_h1sample-0vsrest-df4' : 'CR9114_h1sample-0vsrest-df4',
'CR9114_h1sample-3vsrest-df4' : 'CR9114_h1sample-3vsrest-df4',
'CR9114_h1sample-1vsrest-df2' : 'CR9114_h1sample-1vsrest-df2',
'CR9114_h1sample-1vsrest-df1' : 'CR9114_h1sample-1vsrest-df1',
'CR9114_h1sample-2vsrest-df4' : 'CR9114_h1sample-2vsrest-df4',
'CR9114_h1sample-1vsrest-df3' : 'CR9114_h1sample-1vsrest-df3',
'CR9114_h1sample-2vsrest-df1' : 'CR9114_h1sample-2vsrest-df1',
'CR9114_h1sample-1vsrest-df5' : 'CR9114_h1sample-1vsrest-df5',
'CR9114_h1sample-3vsrest-df3' : 'CR9114_h1sample-3vsrest-df3',
'CR9114_h1sample-0vsrest-df1' : 'CR9114_h1sample-0vsrest-df1',
'CR9114_h1sample-2vsrest-df5' : 'CR9114_h1sample-2vsrest-df5',
'CR9114_h1sample-0vsrest-df2' : 'CR9114_h1sample-0vsrest-df2',

'CreiLOV_sample-2vsrest-df3' : 'CreiLOV_sample-2vsrest-df3',
'CreiLOV_sample-0vsrest-df3' : 'CreiLOV_sample-0vsrest-df3',
'CreiLOV_sample-3vsrest-df2' : 'CreiLOV_sample-3vsrest-df2',
'CreiLOV_sample-2vsrest-df2' : 'CreiLOV_sample-2vsrest-df2',
'CreiLOV_sample-1vsrest-df5' : 'CreiLOV_sample-1vsrest-df5',
'CreiLOV_sample-1vsrest-df1' : 'CreiLOV_sample-1vsrest-df1',
'CreiLOV_sample-3vsrest-df5' : 'CreiLOV_sample-3vsrest-df5',
'CreiLOV_sample-3vsrest-df3' : 'CreiLOV_sample-3vsrest-df3',
'CreiLOV_sample-3vsrest-df4' : 'CreiLOV_sample-3vsrest-df4',
'CreiLOV_sample-1vsrest-df2' : 'CreiLOV_sample-1vsrest-df2',
'CreiLOV_sample-0vsrest-df5' : 'CreiLOV_sample-0vsrest-df5',
'CreiLOV_sample-0vsrest-df1' : 'CreiLOV_sample-0vsrest-df1',
'CreiLOV_sample-2vsrest-df5' : 'CreiLOV_sample-2vsrest-df5',
'CreiLOV_sample-2vsrest-df1' : 'CreiLOV_sample-2vsrest-df1',
'CreiLOV_sample-1vsrest-df4' : 'CreiLOV_sample-1vsrest-df4',
'CreiLOV_sample-2vsrest-df4' : 'CreiLOV_sample-2vsrest-df4',
'CreiLOV_sample-0vsrest-df2' : 'CreiLOV_sample-0vsrest-df2',
'CreiLOV_sample-0vsrest-df4' : 'CreiLOV_sample-0vsrest-df4',
'CreiLOV_sample-1vsrest-df3' : 'CreiLOV_sample-1vsrest-df3',
'CreiLOV_sample-3vsrest-df1' : 'CreiLOV_sample-3vsrest-df1',


    }

def create_parser():
    parser = argparse.ArgumentParser(description="train esm")
    parser.add_argument("split", type=str)
    parser.add_argument("model", choices = ["ridge", "cnn", "esm1b", "esm1v", "esm_rand"], type = str)
    parser.add_argument("gpu", type=str, nargs='?', default='0')
    parser.add_argument("--mean", action="store_true")
    parser.add_argument("--mut_mean", action="store_true")
    parser.add_argument("--flip", action="store_true") # for flipping mut-des and des-mut
    parser.add_argument("--ensemble", action="store_true") 
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument('--kernel_size', type=int, default=5)
    parser.add_argument('--input_size', type=int, default=1024)
    parser.add_argument('--dropout', type=float, default=0.0)
    parser.add_argument('--alpha', type=float, default=1.0)
    parser.add_argument('--gb1_shorten', action="store_true")

    return parser

def train_eval(dataset, model, split, device, mean, mut_mean, batch_size, flip, lr, kernel_size, input_size, dropout, alpha, gb1_shorten): 
    
    results_dir = Path(RESULTS_DIR) 
    EVAL_PATH = results_dir / dataset / model / split
    EVAL_PATH.mkdir(parents=True, exist_ok=True)

    if model.startswith('esm'): 
        kernel_size = input_size = dropout = alpha = '' # get rid of unused variables
        # load data
        train_data, val_data, test_data, max_length = load_esm_dataset(dataset, model, split, mean, mut_mean, flip, gb1_shorten=gb1_shorten)     
        train_iterator = DataLoader(train_data, batch_size=batch_size, shuffle=True)
        #val_iterator = DataLoader(val_data, batch_size=batch_size, shuffle=True)
        test_iterator = DataLoader(test_data, batch_size=batch_size, shuffle=True)
        if len(val_data) > 0:
            val_iterator = DataLoader(val_data, batch_size=batch_size, shuffle=True)
        else:
            val_iterator = None
        # initialize model
        if mean or mut_mean: 
            esm_linear = ESMAttention1dMean(d_embedding=1280)
            mean = True
        else:
            esm_linear = ESMAttention1d(max_length=max_length, d_embedding=1280)   
        # create optmizer and loss function
        optimizer = optim.Adam(esm_linear.parameters(), lr=lr)
        criterion = nn.MSELoss() 
        # train and pass back epochs
        epochs_trained = train_esm(train_iterator, val_iterator, esm_linear, device, criterion, optimizer, 500, mean) 
        # evaluate
        #train_rho, train_mse = evaluate_esm(train_iterator, esm_linear, device, len(train_data), mean, mut_mean, EVAL_PATH / 'test')
        #test_rho, test_mse = evaluate_esm(test_iterator, esm_linear, device, len(test_data), mean, mut_mean, EVAL_PATH / 'train')        
        train_rho, train_mse = evaluate_esm(train_iterator, esm_linear, device, len(train_data), mean, mut_mean, EVAL_PATH / 'train')
        test_rho, test_mse = evaluate_esm(test_iterator, esm_linear, device, len(test_data), mean, mut_mean, EVAL_PATH / 'test')        
        val_rho, val_mse = evaluate_esm(val_iterator, esm_linear, device, len(val_data), mean, mut_mean, EVAL_PATH / 'val')        
        
        if mean:
            model+='_mean'
        if mut_mean:
            model+='_mut_mean'
        if flip:
            split+='_flipped'
        

    if model == 'cnn':
        lr = alpha = '' # get rid of unused variables
        # load data
        train, val, test, _ = load_dataset(dataset, split+'.csv', gb1_shorten=gb1_shorten)
        collate = ASCollater(vocab, Tokenizer(vocab), pad=True)
        if dataset == 'meltome': 
            batch_size = 30 # smaller batch sizes for meltome since seqs are long
        train_iterator = DataLoader(SequenceDataset(train), collate_fn=collate, batch_size=batch_size, shuffle=True, num_workers=4)
        val_iterator = DataLoader(SequenceDataset(val), collate_fn=collate, batch_size=batch_size, shuffle=True, num_workers=4)
        test_iterator = DataLoader(SequenceDataset(test), collate_fn=collate, batch_size=batch_size, shuffle=True, num_workers=4)
        # initialize model
        cnn_model = FluorescenceModel(len(vocab), kernel_size, input_size, dropout) 
        # create optimizer and loss function
        optimizer = optim.Adam([
            {'params': cnn_model.encoder.parameters(), 'lr': 1e-3, 'weight_decay': 0},
            {'params': cnn_model.embedding.parameters(), 'lr': 5e-5, 'weight_decay': 0.05},
            {'params': cnn_model.decoder.parameters(), 'lr': 5e-6, 'weight_decay': 0.05}
        ])
        criterion = nn.MSELoss()
        # train and pass back epochs trained - for CNN, save model 
        epochs_trained = train_cnn(train_iterator, val_iterator, cnn_model, device, criterion, optimizer, 100, EVAL_PATH)
        # evaluate
        train_rho, train_mse = evaluate_cnn(train_iterator, cnn_model, device, EVAL_PATH, EVAL_PATH / 'train')
        test_rho, test_mse = evaluate_cnn(test_iterator, cnn_model, device, EVAL_PATH, EVAL_PATH / 'test')         
        val_rho, val_mse = evaluate_cnn(val_iterator, cnn_model, device, EVAL_PATH, EVAL_PATH / 'val')         

    
    if model == 'ridge':
        lr = kernel_size = input_size = dropout = ''
        # load data
        train, test, max_length = load_dataset(dataset, split+'.csv', val_split = False, gb1_shorten=gb1_shorten)
        train_seq, train_target = get_data(train, max_length, encode_pad=False, one_hots=True)
        test_seq, test_target = get_data(test, max_length, encode_pad=False, one_hots=True)
        # initialize model
        lr_model = RidgeRegression(solver='lsqr', tol=1e-4, max_iter=1e6, alpha=alpha)
        # train and pass back trained model
        lr_trained, epochs_trained = train_ridge(train_seq, train_target, lr_model)
        # evaluate
        train_rho, train_mse = evaluate_ridge(train_seq, train_target, lr_trained, EVAL_PATH / 'train')
        test_rho, test_mse = evaluate_ridge(test_seq, test_target, lr_trained, EVAL_PATH / 'test')

    print('done training and testing: dataset: {0} model: {1} split: {2} \n'.format(dataset, model, split))
    print('full results saved at: ', EVAL_PATH) 
    print('train stats: Spearman: %.2f MSE: %.2f ' % (train_rho, train_mse))
    print('test stats: Spearman: %.2f MSE: %.2f ' % (test_rho, test_mse))

    with open(results_dir / (dataset+'_results.csv'), 'a', newline='') as f:
        writer(f).writerow([dataset, model, split, train_rho, train_mse, test_rho, test_mse, epochs_trained, lr, kernel_size, input_size, dropout, alpha, gb1_shorten])


def main(args):
    device = torch.device('cpu')
    device = torch.device('cuda:'+args.gpu)
    split = split_dict[args.split]
    dataset = re.findall(r'(\w*)\_', args.split)[0]

    print('dataset: {0} model: {1} split: {2} \n'.format(dataset, args.model, split)) 

    if args.ensemble: # run training and evaluation on 10 different random seeds 
        for i in range(10):
            random.seed(i)
            torch.manual_seed(i)
            train_eval(dataset, args.model, split, device, args.mean, args.mut_mean, 256, args.flip, args.lr, args.kernel_size, args.input_size, args.dropout, args.alpha, args.gb1_shorten)
    else: 
        random.seed(10)
        torch.manual_seed(10)
        train_eval(dataset, args.model, split, device, args.mean, args.mut_mean, 256, args.flip, args.lr, args.kernel_size, args.input_size, args.dropout, args.alpha, args.gb1_shorten)

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    main(args)

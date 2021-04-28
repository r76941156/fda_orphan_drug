import pandas as pd
import os
import csv
import numpy as np
import json

from biothings import config
from biothings.utils.dataload import dict_convert, dict_sweep
logging = config.logger

def load_data(data_folder):
    f = open('data.json',)
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    f.close()
    return data



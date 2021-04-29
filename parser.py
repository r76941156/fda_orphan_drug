import pandas as pd
import os
import csv
import numpy as np
import json

from biothings import config
from biothings.utils.dataload import dict_convert, dict_sweep
logging = config.logger

def load_data(data_folder):
    infile = os.path.join(data_folder,"data.json")
    f = open(infile)
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    f.close()
    yield data



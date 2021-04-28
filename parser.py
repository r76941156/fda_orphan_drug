import pandas as pd
import os
import csv
import numpy as np

from biothings import config
from biothings.utils.dataload import dict_convert, dict_sweep
logging = config.logger

def load_data(data_folder):
    infile = os.path.join(data_folder,"compound.csv")
    assert os.path.exists(infile)
    dat = pd.read_csv(infile).to_dict('records')
    for rec in dat:
         rec = dict_sweep(rec,vals=[np.nan])

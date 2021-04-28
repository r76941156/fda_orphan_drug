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
    #dat = pd.read_csv(infile,sep="\t").to_dict('records')
    dat = pd.read_csv(infile).to_dict('records')
    results={}
    for rec in dat:
         rec = dict_sweep(rec,vals=[np.nan])
    for rec in dat:
         _id=rec['_id']
         del rec['_id']
         results.setdefault(_id,[]).append(rec)
    #print(results['GJPICJJJRGTNOD-UHFFFAOYSA-N'])

    for _id,docs in results.items():
        doc = {"_id": _id, "Orphan Drug Designations" : docs}
        yield doc

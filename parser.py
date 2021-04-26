import pandas as pd
import os
import csv

#print(pd.__version__)

from biothings import config
from biothings.utils.dataload import dict_convert
logging = config.logger

def load_data(data_folder):
    infile = os.path.join(data_folder,"compound.csv")
    assert os.path.exists(infile)
    #dat = pd.read_csv(infile,sep="\t",squeeze=True,quoting=csv.QUOTE_NONE).to_dict('records')
    dat = pd.read_csv(infile,sep="\t",quoting=csv.QUOTE_NONE).to_dict('records')
    #results = {}
    #for rec in dat:
        #print(rec)
        #print("=======")

#load_data("./")

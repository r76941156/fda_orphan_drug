import os.path
import json


def load_data(data_folder):
    infile = os.path.join(data_folder,"data.json")
    f = open(infile)
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    f.close()
    for doc in data:
        yield doc



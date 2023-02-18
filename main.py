from data_handler import *
import csv
import pandas as pd
from scripts import *

resumes: list[dict] = parse_resumes("junior python dev")
keys = list(resumes[0].keys())
dict_list_to_csv(resumes, "table", keys)

dataframe = pd.read_csv('table.csv')
print(sort(dataframe, "age"))
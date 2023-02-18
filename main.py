from data_handler import *
import csv
import pandas as pd
from scripts import *


parse_resumes('junior python dev')
dataframe = pd.read_csv('table.csv')
print(dataframe)
from data_handler import *
import csv
import pandas as pd

resumes: list[dict] = get_resumes_list("java")
keys = list(resumes[0].keys())

dict_list_to_csv(resumes, "table", keys)
output_table("table")
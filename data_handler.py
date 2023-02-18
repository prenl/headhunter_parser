from hh_parser import *
import pandas as pd
import csv

def dict_list_to_csv(dict_list:list[dict], file_name: str, keys: list[str]):
    with open(file_name + ".csv", "w", newline="", encoding="UTF-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        for row in dict_list or []:
            writer.writerow(row)
    print("CSV file created successfully")
    return

def get_resumes_list(job_title):
    resumes: list[dict] = []
    links = findLinks(job_title)
    for link in links:
        resumes.append(dict(parse_link(link)))
    return resumes

def output_table(table_name):
    pd.set_option('display.max_columns', 10)
    pd.options.display.expand_frame_repr = False
    df = pd.read_csv(table_name + ".csv")
    print(df)
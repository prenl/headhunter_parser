from hh_parser import parse_link, findLinks
import csv
import pandas as pd

def dict_list_to_csv(dict_list:list[dict], file_name: str, keys: list[str]):
    with open(file_name + ".csv", "w", newline="", encoding="UTF-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        for row in dict_list or []:
            writer.writerow(row)

def get_resumes_list(job_title):
    resumes: list[dict] = []
    links = findLinks(job_title)
    for link in links:
        resumes.append(dict(parse_link(link)))
    return resumes


resumes: list[dict] = get_resumes_list("java")

keys = list(resumes[0].keys())
dict_list_to_csv(resumes, "table", keys)

df = pd.read_csv("table.csv")
print(df)
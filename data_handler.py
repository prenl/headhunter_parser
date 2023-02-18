from hh_parser import *
import pandas as pd
import csv


def parse_resumes(job_title: str):
    links = find_links(job_title)

    with open('table.csv', 'a+', newline='', encoding="utf-8") as writer_obj:
        resume = dict(parse_link(links[0]))
        csv_writer = csv.writer(writer_obj)
        csv_writer.writerow(resume.keys())
        csv_writer.writerow(resume.values())
            
    for i in range(1, len(links)):
        resume = dict(parse_link(links[i]))
        with open('table.csv', 'a+', newline='', encoding="utf-8", ) as writer_obj:
            csv_writer = csv.writer(writer_obj)
            csv_writer.writerow(resume.values())

    print("CSV FILE CREATED SUCCESSFULLY")
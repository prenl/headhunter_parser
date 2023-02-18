import requests
from bs4 import BeautifulSoup
import re


def find_links(job_title:str) -> list[str]:
    links = []
    page = 1
    source_url = f"https://hh.kz/search/resume?area=40&currency_code=KZT&exp_period=all_time&logic=normal&no_magic=true&order_by=relevance&ored_clusters=true&pos=full_text&text={job_title}&items_on_page=100&page={page}"
    while len(links) < 10:
        source_html = requests.get(source_url, headers={'User-Agent': 'Custom'})
        source_soup = BeautifulSoup(source_html.text, 'html.parser')
        for block in source_soup.findAll('span', attrs={'class': 'bloko-header-section-3'}):
            link = "https://hh.kz/" + block.find('a', attrs={'class': 'serp-item__title'}).get('href').split('?')[0]
            links.append(link)
            if len(links) >= 10:
                break
        page += 1
    return links


def parse_link(link: str) -> dict:
    link_html = requests.get(link, headers={'User-Agent': 'Custom'})
    link_soup = BeautifulSoup(link_html.text, 'html.parser')
    
    # finding title
    if len(link_soup.findAll('span', attrs={'class': 'resume-block__title-text', 'data-qa': "resume-block-title-position"})) == 0:
        title = "Unspecified"
    for block in link_soup.findAll('span', attrs={'class': 'resume-block__title-text', 'data-qa': "resume-block-title-position"}):
        title = block.text
    

    # finding specialization
    if len(link_soup.findAll('li', attrs={'class': 'resume-block__specialization'})) == 0:
        specialization = "Unspecified"
    for block in link_soup.findAll('li', attrs={'class': 'resume-block__specialization'}):
        specialization = block.text
    

    # finding salary
    if len(link_soup.findAll('span', attrs={'class': 'resume-block__salary'})) == 0:
        salary = "Unspecified"
    else:
        for block in link_soup.findAll('span', attrs={'class': 'resume-block__salary'}):
            salary = block.text
            salary = "".join(i for i in salary if i.isdigit())

    # finding age
    if len(link_soup.findAll('span', attrs={'data-qa': 'resume-personal-age'})) == 0:
        age = "Unspecified"
    else:
        age = link_soup.findAll('span', attrs={'data-qa': 'resume-personal-age'})[0].text
        age = "".join(i for i in age if i.isdigit())

    # finding employment
    for block in link_soup.findAll('div', attrs={'class': 'resume-block-container'}):
        if "Занятость" in block.text:
            employment = block.text.split('Занятость: ')[1].split('График работы:')[0]
            break
        elif "Employment" in block.text:
            employment = block.text.split('Employment: ')[1].split('Work schedule:')[0]
            break
        else:
            employment = 'Unspecified'

    # finding schedule
    for block in link_soup.findAll('div', attrs={'class': 'resume-block-container'}):
        if "График" in block.text:
            schedule = block.text.split('График работы: ')[1]
            break
        elif "schedule" in block.text:
            schedule = block.text.split('schedule: ')[1]
            break
        else:
            schedule = 'Unspecified'

    # finding experience
    experience_years = "Unspecified"
    experience_months = "Unspecified"
    for block in link_soup.findAll('span', attrs={'class': 'resume-block__title-text resume-block__title-text_sub'}):
        if "Опыт" in block.text or "experience" in block.text:
            experience = re.findall(r'\b\d+\b', block.text)
            if len(experience) == 2:
                experience_years = experience[0]
                experience_months = experience[1]
            elif len(experience) == 1:
                experience_years = experience[0]
            else:
                break

    # finding citizenship
    for block in link_soup.findAll('div', attrs={'class': 'resume-block-container'}):
        if not block.find('p') is None:
            citizenship = block.find('p').text[13:]

    # finding sex
    if len(link_soup.findAll('span', attrs={'data-qa': 'resume-personal-gender'})) == 0:
        sex = "Unspecified"
    else:
        sex = link_soup.findAll('span', attrs={'data-qa': 'resume-personal-gender'})[0].text

    resume = {
        'title': title,
        'specialization': specialization,
        'salary': salary,
        'age': age,
        'employment': employment,
        'schedule': schedule,
        'experience_years': experience_years,
        'experience_months': experience_months,
        'citizenship': citizenship,
        'sex': sex,
        'link': link
    }

    print(resume)
    return resume
    
# print(parse_link("https://hh.kz/resume/c5ffe3dc00063777b90039ed1f4f566e546755"))
# HEADHUNTER RESUME PARSER
# BY ABDRAKHMANOV YELNUR AND ANANYAN KAREN
# SE-2203, ASTANA IT UNIVERSITY
# 2023
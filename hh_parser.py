import requests
from bs4 import BeautifulSoup
import re
import time

def find_links(job_title:str, number_of_links: int) -> list[str]:
    job_title.replace(" ", "+")
    links = []

    url = f"https://hh.kz/search/resume?text={job_title}&area=40&currency_code=KZT&no_magic=true&ored_clusters=true&order_by=relevance&logic=normal&pos=full_text&exp_period=all_time"
    html = requests.get(url, headers={'User-Agent': 'Custom'})
    soup = BeautifulSoup(html.text, 'html.parser')
    
    try:
        page_count = int(soup.find('div', attrs={'class': 'pager'}).find_all('span', recursive=False)[-1].find('a').find('span').text)
    except AttributeError:
        page_count = 0
        for block in soup.findAll('a', attrs={'class': 'serp-item__title'}):
            link = "https://hh.kz" + block.get('href').split('?')[0]
            links.append(link)
            print(link)
            if len(links) >= number_of_links:
                return links
        print('\n' * 10)
        return links


    for page in range(page_count):
        url = f"https://hh.kz/search/resume?text={job_title}&area=40&currency_code=KZT&no_magic=true&ored_clusters=true&order_by=relevance&logic=normal&pos=full_text&exp_period=all_time&page={page}"
        html = requests.get(url, headers={'User-Agent': 'Custom'})
        soup = BeautifulSoup(html.text, 'html.parser')

        for block in soup.findAll('a', attrs={'class': 'serp-item__title'}):
            link = "https://hh.kz" + block.get('href').split('?')[0]
            links.append(link)
            if len(links) >= number_of_links:
                return links

        time.sleep(1)

    return links


def parse_link(link: str) -> dict:
    link_html = requests.get(link, headers={'User-Agent': 'Custom'})
    link_soup = BeautifulSoup(link_html.text, 'html.parser')
    

    # finding title
    title = None
    for block in link_soup.findAll('span', attrs={'class': 'resume-block__title-text', 'data-qa': "resume-block-title-position"}):
        title = block.text
    

    # finding specialization
    specialization = None
    for block in link_soup.findAll('li', attrs={'class': 'resume-block__specialization'}):
        specialization = block.text
    

    # finding salary
    salary = None
    for block in link_soup.findAll('span', attrs={'class': 'resume-block__salary'}):
        salary = block.text
        if "USD" in salary:
            salary = "".join(i for i in salary if i.isdigit())
            salary = str(int(float(salary) * 444.07))
            # current exchange rate from INVESTING.COM
            # 1 USD   <===>   444.07 KZT
        elif "EUR" in salary:
            salary = "".join(i for i in salary if i.isdigit())
            salary = str(int(float(salary) * 478.135))
            # current exchange rate from INVESTING.COM
            # 1 EUR   <===>   478.135 KZT
        else:
            salary = "".join(i for i in salary if i.isdigit())


    # finding age
    if len(link_soup.findAll('span', attrs={'data-qa': 'resume-personal-age'})) != 0:
        age = link_soup.findAll('span', attrs={'data-qa': 'resume-personal-age'})[0].text
        age = "".join(i for i in age if i.isdigit())
    else:
        age = None
        

    # finding employment
    employment = None
    for block in link_soup.findAll('div', attrs={'class': 'resume-block-container'}):
        if "Занятость" in block.text:
            employment = block.text.split('Занятость: ')[1].split('График работы:')[0]
            break
        elif "Employment" in block.text:
            employment = block.text.split('Employment: ')[1].split('Work schedule:')[0]
            break


    # finding schedule
    schedule = None
    for block in link_soup.findAll('div', attrs={'class': 'resume-block-container'}):
        if "График" in block.text:
            schedule = block.text.split('График работы: ')[1]
            break
        elif "schedule" in block.text:
            schedule = block.text.split('schedule: ')[1]
            break
            

    # finding experience
    experience_years = 0
    experience_months = 0
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
    citizenship = None
    for block in link_soup.findAll('div', attrs={'class': 'resume-block-container'}):
        if not block.find('p') is None:
            citizenship = block.find('p').text[13:]
            if "Kazakhstan" in citizenship:
                citizenship = "Казахстан"
            elif "Russia" in citizenship:
                citizenship = "Россия"
            elif "Uzbekistan" in citizenship:
                citizenship = "Узбекистан"
        else:
            citizenship = None


    # finding sex
    if len(link_soup.findAll('span', attrs={'data-qa': 'resume-personal-gender'})) == 0:
        sex = None
    else:
        sex = link_soup.findAll('span', attrs={'data-qa': 'resume-personal-gender'})[0].text
        if "Male" in sex:
            sex = True
        else:
            sex = False


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
    
# HEADHUNTER RESUME PARSER
# BY ABDRAKHMANOV YELNUR, ANANYAN KAREN AND ASLAN JELEUBAY
# SE-2203, ASTANA IT UNIVERSITY
# 2023
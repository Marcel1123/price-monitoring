import requests
import csv
import os
from bs4 import BeautifulSoup
from web_scraper.real_estates import real_estates


# This scraper was taken from this tutorial: https://realpython.com/beautiful-soup-web-scraper-python/
def scraper_from_tutorial(export_path=None):
    return_list = []
    URL = real_estates['tutorial_url']
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='ResultsContainer')
    job_elems = results.find_all('section', class_='card-content')
    for job_elem in job_elems:
        title_elem = job_elem.find('h2', class_='title')
        company_elem = job_elem.find('div', class_='company')
        location_elem = job_elem.find('div', class_='location')
        if None in (title_elem, company_elem, location_elem):
            continue
        result_dict = dict()
        result_dict['title'] = title_elem.text.strip()
        result_dict['company'] = company_elem.text.strip()
        result_dict['location'] = location_elem.text.strip()
        return_list.append(result_dict)
    export_scraper_results_csv(return_list, export_path)
    return return_list


# This scraper was made to test the libraries and obtain static results for unit tests
def static_scraper(export_path=None):
    return_list = []
    URL = real_estates['static_url']
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='col-lg-4')
    for result in results:
        price = result.find('h4', class_='price')
        title = result.find('a', class_='title')
        description = result.find('p', class_='description')
        reviews = result.find('p', class_='pull-right')
        if None in (price, title, description, reviews):
            continue
        result_dict = dict()
        result_dict['price'] = price.text.strip()
        result_dict['title'] = title.text.strip()
        result_dict['description'] = description.text.strip()
        result_dict['reviews'] = reviews.text.strip()
        return_list.append(result_dict)
    export_scraper_results_csv(return_list, export_path)
    return return_list


def export_scraper_results_csv(dict_list, export_path):
    if export_path is None:
        return
    if os.path.exists(export_path):
        os.remove(export_path)
    keys = dict_list[0].keys()
    with open(export_path, 'w', newline='') as export_file:
        dict_writer = csv.DictWriter(export_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dict_list)


if __name__ == '__main__':
    static_scraper('../../Data/test.csv')

import random
import time
import requests
import csv
import os
from datetime import date
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


def imobiliare_ro_scraper(export_path=None, given_city='iasi', houses=False, page_number=101):
    return_list = []
    city = given_city.capitalize()
    if houses is False:
        URL = real_estates['imobiliare_ro_apartamente'] + given_city
    else:
        URL = real_estates['imobiliare_ro_case'] + given_city
    today = date.today()
    current_date = today.strftime("%B %d, %Y")
    current_date_for_path = today.strftime("%d-%m-%Y")

    # get info from given number of pages (30 products/page)
    for i in range(1, page_number):
        print(i)
        URL_with_page = URL + '?pagina=' + str(i)
        page = requests.get(URL_with_page)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('div', class_='col-lg-8 col-md-8 col-sm-9 col-xs-12 box-height')
        for result in results:
            # get url
            url_link = result.find('a', href=True)
            url_link = url_link['href']

            # get title
            # potential_titles = result.find_all('a')
            # title = 'N/A'
            # for potential_title in potential_titles:
            #     title = potential_title.get('title', 'N/A')
            #     if title != 'N/A':
            #         break
            # title = title.replace('ş', 's')
            # title = title.replace('ă', 'a')
            # title = title.replace('ţ', 't')

            # get price
            try:
                price = result.find('span', class_='pret-mare')
                price = price.text.strip()
            except AttributeError:
                price = 'N/A'

            # get location
            location = ''
            location_find = result.find('div', class_='localizare')
            location_find = location_find.find('p').text.split()[2:]
            for word in location_find:
                location += word + ' '
            location = location.replace('ş', 's')
            location = location.replace('ă', 'a')
            location = location.replace('ţ', 't')

            # go in sub-page
            time.sleep(random.uniform(1.05, 5.45))
            sub_page = requests.get(url_link)
            sub_soup = BeautifulSoup(sub_page.content, 'html.parser')
            sub_results = sub_soup.find_all('ul', class_='lista-tabelara')
            first_row = sub_results[0].find_all('li')

            update_date = sub_soup.find('span', class_='data-actualizare')
            update_date = update_date.text.strip()

            if 'nemobilat' in sub_soup.text.lower():
                furnish_type = 'Unfurnished'
            elif 'mobilat' in sub_soup.text.lower():
                furnish_type = 'Furnished'
            else:
                furnish_type = 'N/A'

            # give default values to product properties
            nr_of_rooms = 'N/A'
            size = 'N/A'
            product_type = 'House'
            floor_number = 'N/A'
            nr_of_floors = 'N/A'
            year_of_construction = 'N/A'

            for li in first_row:
                if 'Nr. camere' in li.text:
                    nr_of_rooms = li.find('span').text.strip()
                elif 'Suprafaţă utilă' in li.text:
                    size = li.find('span').text.strip()
                    try:
                        words = size.split(' ')
                        if ',' in words[0]:
                            nr = words[0].split(',')
                        else:
                            nr = words[0].split('.')
                        if len(nr) == 1:
                            size = nr[0] + ' ' + words[1]
                        else:
                            size = nr[0] + '.' + nr[1] + ' ' + words[1]
                    except:
                        size = 'N/A'
                elif 'Compartimentare' in li.text:
                    product_type = li.find('span').text.strip().lower()
                    if product_type == 'decomandat':
                        product_type = 'Detached'
                    elif product_type == 'nedecomandat' or product_type == 'ne-decomandat' or product_type == 'ne_decomandat':
                        product_type = 'Non_detached'
                    elif product_type == 'semidecomandat' or product_type == 'semi-decomandat' or product_type == 'semi_decomandat':
                        product_type = 'Semi_detached'
                    else:
                        product_type = 'Studio'
                elif 'Etaj' in li.text:
                    try:
                        floor_number = li.find('span').text.strip().split()[1]
                        nr_of_floors = li.find('span').text.strip().split()[3]
                    except IndexError:
                        try:
                            floor_number = li.find('span').text.strip().split()[0]
                            nr_of_floors = li.find('span').text.strip().split()[2]
                        except IndexError:
                            floor_number = li.find('span').text.strip()

            second_row = sub_results[1].find_all('li')
            for li in second_row:
                if 'An construcţie' in li.text:
                    year_of_construction = li.find('span').text.strip()

            result_dict = dict()
            # result_dict['title'] = title
            result_dict['scrap_date'] = current_date
            result_dict['update_date'] = update_date
            result_dict['price'] = price
            result_dict['city'] = city
            result_dict['location'] = location
            result_dict['product_type'] = product_type
            result_dict['furnish_type'] = furnish_type
            result_dict['number_of_rooms'] = nr_of_rooms
            result_dict['floor_number'] = floor_number
            result_dict['number_of_floors'] = nr_of_floors
            result_dict['size'] = size
            result_dict['year_of_construction'] = year_of_construction
            return_list.append(result_dict)
        export_scraper_results_csv(return_list, export_path[:-4] + '_' + current_date_for_path + '_' + str(i) + '.csv')
    export_scraper_results_csv(return_list, export_path)
    return return_list


def export_scraper_results_csv(dict_list, export_path):
    if export_path is None:
        return
    if os.path.exists(export_path):
        os.remove(export_path)
    keys = dict_list[0].keys()
    with open(export_path, 'w', newline='', encoding="iso8859_2") as export_file:
        dict_writer = csv.DictWriter(export_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dict_list)


def delete_title_from_imobiliare_ro_csv(path):
    with open(path, "rt", encoding="iso8859_2") as source:
        rdr = csv.reader(source)
        with open(path[:-4] + '_no_title' + '.csv', "wt", encoding="iso8859_2", newline='') as result:
            wtr = csv.writer(result)
            for r in rdr:
                wtr.writerow((r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12]))


def remove_empty_rows_from_csv(path):
    with open(path, "rt", encoding="iso8859_2") as in_file:
        with open(path[:-4] + '_no_empty_rows' + '.csv', "w", encoding="iso8859_2", newline='') as result:
            writer = csv.writer(result)
            for row in csv.reader(in_file):
                if row:
                    writer.writerow(row)


def update_size_from_imobiliare_ro_csv(path):
    index = 0
    with open(path, "rt", encoding="iso8859_2") as source:
        rdr = csv.reader(source)
        with open(path[:-4] + '_new_size' + '.csv', "wt", encoding="iso8859_2", newline='') as result:
            wtr = csv.writer(result)
            for r in rdr:
                size = r[10]
                if index > 0:
                    try:
                        words = size.split(' ')
                        if ',' in words[0]:
                            nr = words[0].split(',')
                        else:
                            nr = words[0].split('.')
                        if len(nr) == 1:
                            size = nr[0] + ' ' + words[1]
                        else:
                            size = nr[0] + '.' + nr[1] + ' ' + words[1]
                    except:
                        size = 'N/A'
                wtr.writerow((r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], size, r[11]))
                index += 1


if __name__ == '__main__':
    # static_scraper('../../Data/test.csv')
    # imobiliare_ro_scraper('../../Data/imobiliare_ro_apartamente_iasi.csv')
    # delete_title_from_imobiliare_ro_csv('../../Data/imobiliare_ro_apartamente_iasi_15-11-2020.csv')
    # remove_empty_rows_from_csv('../../Data/imobiliare_ro_apartamente_iasi_15-11-2020.csv')
    # update_size_from_imobiliare_ro_csv('../../Data/imobiliare_ro_apartamente_iasi_15-11-2020.csv')
    imobiliare_ro_scraper('../../Data/imobiliare_ro_case_iasi.csv', page_number=21, houses=True)

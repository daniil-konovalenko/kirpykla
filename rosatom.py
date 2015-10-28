import requests
import bs4
import sqlite3
import logging
from service import fill_database


def rosatom():
    result_table = []
    url = ("https://mephi.ru/schoolkids/olimpiads/rosatom/"
           "Pobediteli/pobediteli-fizika-14.php")
    logging.info('Connecting to rosatom website')
    res = requests.get(url)
    assert res.status_code == requests.codes.ok
    logging.info('Connected to rosatom website')
    rosatomsoup = bs4.BeautifulSoup(res.text)

    content = rosatomsoup.find('table', {'id': 'content'})
    table = content.find('table', {'width': 542})
    tbody = table.select('tbody')[0]
    for table_row in tbody.find_all('tr'):
        table_data = [td.text.rstrip().lstrip() for td in table_row.find_all('td')]
        if not table_data[0] or table_data[1] == 'ФИО':
            continue

        name = table_data[1].split()
        logging.debug('name={}'.format(name))
        first_name = name[1]
        second_name = name[2]
        last_name = name[0]
        result = table_data[2]
        title = 'Диплом {} степени'.format(table_data[3])
        school_id = 1
        result_table.append({'first_name': first_name, 'second_name': second_name,
                             'last_name': last_name, 'result': result, 'title': title,
                             'school_id': school_id, 'year': 2014})

    logging.info('Connecting to database')
    results_connection = sqlite3.connect('results.sqlite3')
    service_connection = sqlite3.connect('service.sqlite3')
    logging.info('Connected to database')

    results_cursor = results_connection.cursor()
    service_cursor = service_connection.cursor()

    fill_database(result_table, 'Олимпиада Росатом по физике', results_cursor,
                  service_cursor)
    service_connection.commit()
    service_connection.close()
    results_connection.commit()
    results_connection.close()


if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)
    rosatom()

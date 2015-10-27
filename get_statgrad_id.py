import requests
import bs4
import sqlite3
import logging


def get_ids():
    url = 'http://reg.olimpiada.ru/files/rusolymp-2015/councils.html'
    response = requests.get(url)
    statgrad_soup = bs4.BeautifulSoup(response.content.decode())

    pairs = [line.split(maxsplit = 1) for line in statgrad_soup.select('body')[0] if
             'sch' in line]
    return pairs


def create_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS 'schools' ("
                   "'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                   "'school_name' TEXT,"
                   "'statgrad_id' INTEGER);")


def fill_statgrad_ids(cursor):
    logging.info('Creating table')
    create_table(cursor)
    logging.info('Table was created successfully')

    pairs = get_ids()
    for pair in pairs:
        cursor.execute("INSERT INTO schools VALUES (NULL, :school_name, :statgrad_id)",
                       {'school_name': pair[1].upper(),
                        'statgrad_id': pair[0].lstrip('sch')})

    logging.info('School ids filled in successfully')


if __name__ == '__main__':
    logging.basicConfig(format = '%(msg)s', level = logging.INFO)
    service_database = 'service.sqlite3'
    service_connection = sqlite3.connect(service_database)
    service_cursor = service_connection.cursor()
    fill_statgrad_ids(service_cursor)
    service_connection.commit()
    service_connection.close()

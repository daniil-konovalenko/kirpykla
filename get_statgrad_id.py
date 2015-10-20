import requests
import bs4
import sqlite3
import logging


logging.basicConfig(format='%(msg)s', level=logging.INFO)

def get_ids():
    url = 'http://reg.olimpiada.ru/files/rusolymp-2015/councils.html'
    response = requests.get(url)
    statgrad_soup = bs4.BeautifulSoup(response.content.decode())

    pairs = [line.split(maxsplit=1) for line in statgrad_soup.select('body')[0] if 'sch' in line]
    return pairs


def create_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS 'schools' ("
                    "'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                    "'school_name' TEXT,"
                    "'statgrad_id' INTEGER);")



if __name__ == '__main__':
    pairs = get_ids()

    connection = sqlite3.connect('service.sqlite3')
    cursor = connection.cursor()

    logging.info('Creating table')
    create_table(cursor)
    logging.info('Table was created successfully')
    for pair in pairs:
        cursor.execute("INSERT into schools VALUES (NULL, :school_name, :statgrad_id)",
                       {'school_name': pair[1], 'statgrad_id': pair[0].lstrip('sch')})
    connection.commit()
    connection.close()
    logging.info('School ids filled in successfully')




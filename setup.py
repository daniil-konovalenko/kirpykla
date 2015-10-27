import os.path
import logging
import sqlite3
from get_statgrad_id import fill_statgrad_ids


def create_database(db_path):
    if os.path.exists(db_path):
        logging.critical('Are you sure you want to override the database? [y/n]')
        user_reaction = input()
        if user_reaction.upper() == 'Y':
            with open(db_path, 'w') as file:
                logging.info('Database created')
        else:
            exit('Database already exists')


def main(results_database, service_database):
    logging.info('Creating the results database')
    create_database(results_database)
    logging.info('Creating the service database')
    create_database(service_database)

    service_connection = sqlite3.connect(service_database)
    service_cursor = service_connection.cursor()
    service_cursor.execute("CREATE TABLE 'students' ("
                           "'id'	INTEGER PRIMARY KEY AUTOINCREMENT,"
                           "'first_name'	TEXT,"
                           "'second_name'	TEXT,"
                           "'last_name'	TEXT,"
                           "'school_id'	INTEGER)")
    logging.debug('Created students table')

    fill_statgrad_ids(service_cursor)


if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG,
                        format = '%(asctime)s - %(levelname)s: %(message)s')

    # TODO: Add config file or command line args parsing
    results_db = 'results.sqlite3'
    service_db = 'service.sqlite3'
    main(results_db, service_db)

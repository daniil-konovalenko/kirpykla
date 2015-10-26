import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

def get_results(student_data, cursor):
    response = cursor.execute("SELECT name from sqlite_master WHERE type = 'table';")

    tables = set(response.fetchall()) - {('students',), ('sqlite_sequence',)}
    logging.debug(tables)


    student_id_response = cursor.execute("SELECT id FROM students WHERE "
                                         "first_name=:first_name AND "
                                         "second_name=:second_name AND "
                                         "last_name=:last_name AND "
                                         "school_id=:school_id", student_data).fetchone()
    if not student_id_response:
        return {'status': 'NOT FOUND'}
    student_id = student_id_response[0]
    results_table = []
    for table in tables:
        olymp = table[0]
        query = "SELECT result, title, year from '{}' WHERE student_id = ?".format(olymp)
        logging.debug(student_id)
        logging.debug(query)
        result_response = cursor.execute(query, (student_id, ))
        for result_row in result_response:
            result = result_row[0]
            title = result_row[1]
            year = result_row[2]

            results_table.append([olymp, result, title, year])

    return {'status': 'OK', 'table': results_table}

def add_table(cursor, table_name):
    # Adds an olympiad results table to the specified database
    cursor.execute("CREATE TABLE IF NOT EXISTS '{}' ("
                   "'id' INTEGER PRIMARY KEY AUTOINCREMENT, "
                   "'student_id' INTEGER,"
                   "'year' INTEGER,"
                   "'result' TEXT,"
                   "'title' TEXT"
                   ");".format(table_name))


def fill_database(results_table, olymp_name, cursor):
    """
    results_table = {first_name: , second_name, last_name, school_id, }
    """
    try:
        add_table(cursor, olymp_name)
    except sqlite3.OperationalError:
        logging.info('Table already exists')

    for result_row in results_table:
        cursor.execute("INSERT into 'students' VALUES (NULL, :first_name, :second_name, "
                       ":last_name, :school_id)", result_row)

        result_row['student_id'] = cursor.lastrowid

        cursor.execute("INSERT into '{}' VALUES (NULL, :student_id, :year, "
                       "                                 :result, :title)".format(olymp_name), result_row)




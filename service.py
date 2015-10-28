import logging


def get_results(student_data, results_cursor, service_cursor):
    response = results_cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")

    tables = set(response.fetchall()) - {('students',), ('sqlite_sequence',)}
    logging.debug('Found tables: {}'.format(tables))

    student_id_response = service_cursor.execute("SELECT id FROM students WHERE "
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
        query = "SELECT result, title, year FROM '{}' WHERE student_id = ?".format(olymp)
        logging.debug(student_id)
        logging.debug(query)
        result_response = results_cursor.execute(query, (student_id,))
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


def fill_database(results_table, olymp_name, results_cursor, service_cursor):
    """
    results_table = {first_name: , second_name, last_name, school_id, }
    """
    add_table(results_cursor, olymp_name)

    for result_row in results_table:
        service_cursor.execute("INSERT INTO 'students' VALUES (NULL, :first_name, "
                               "                                     :second_name,"
                               "                                     :last_name,"
                               "                                     :school_id)",
                               result_row)

        result_row['student_id'] = service_cursor.lastrowid

        results_cursor.execute("INSERT INTO '{}' VALUES (NULL, :student_id, :year, "
                               ":result, :title)".format(olymp_name), result_row)


if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)

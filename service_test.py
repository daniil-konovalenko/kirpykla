import sqlite3
import unittest
from service import add_table, get_results


class ServiceTester(unittest.TestCase):
    def setUp(self):
        self.existing_student = {'first_name': 'Иван',
                                 'second_name': 'Иванович',
                                 'last_name': 'Иванов',
                                 'school_id': 1}
        self.not_existing_student = {'first_name': 'Михаил',
                                     'second_name': 'Алексеевич',
                                     'last_name': 'Калинин',
                                     'school_id': 779004}

        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE 'students' ("
                            "'id' INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "'first_name' TEXT,"
                            "'second_name' TEXT,"
                            "'last_name' TEXT,"
                            "'school_id' INTEGER)")

        self.cursor.execute("CREATE TABLE 'test' ("
                            "'id' INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "'student_id' INTEGER,"
                            "'year' INTEGER,"
                            "'result' TEXT,"
                            "'title' TEXT"
                            ")")

        self.cursor.execute("INSERT into 'students' VALUES "
                            "(NULL, :first_name, :second_name, :last_name, :school_id)",
                            self.existing_student)

        self.cursor.execute("INSERT into 'test' VALUES (NULL, 1, 2007, '100', 'Победитель')")
        
    def tearDown(self):
        self.connection.close()

    def test_add_table(self):
        olymp_name = 'Test olympiad'
        add_table(self.cursor, olymp_name)
        right_sql = ("CREATE TABLE '{}' ("
                     "'id' INTEGER PRIMARY KEY AUTOINCREMENT, "
                     "'student_id' INTEGER,"
                     "'year' INTEGER,"
                     "'result' TEXT,"
                     "'title' TEXT"
                     ")").format(olymp_name)
        real_sql = self.cursor.execute("SELECT sql from sqlite_master WHERE name=?",
                                       (olymp_name, )).fetchone()[0]
        self.assertEqual(real_sql, right_sql)

    def test_get_results(self):
        real_results = get_results(self.existing_student, self.cursor)
        right_results = {'status': 'OK' , 'table': [['test', '100', 'Победитель', 2007]]}
        self.assertEqual(real_results, right_results)

    def test_get_results_not_found(self):
        real_results = get_results(self.not_existing_student, self.cursor)
        right_results = {'status': 'NOT FOUND'}
        self.assertEqual(real_results, right_results)



if __name__ == '__main__':
    unittest.main()

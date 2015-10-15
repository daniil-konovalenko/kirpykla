    import sqlite3

file_name = input('Введите название файла')
file = open(file_name, "r")
table = file.readlines()
for i in range(table):
    table[i] = table[i].split(' ')
class_number = table[0].find('Класс') #Номер столбца с классом. Нужно добавить разные варианты (с большими буквами, с маленькими и т.д. для всего)
status_number = table[0].find('Итог тура')
mark_number = table[0].find('Баллы')
# ещё некоторые виды полей
# Возможно, их надо переделать с try


olymp_name = input("Введите название олимпиады")
con = sqlite3.connect('data.db')
cur = con.cursor()
cur.execute('CREATE TABLE ...')
for i in table[1:]:
    cur.execute('INSERT INTO ...')


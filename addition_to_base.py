    import sqlite3

file_name = input('������� �������� �����')
file = open(file_name, "r")
table = file.readlines()
for i in range(table):
    table[i] = table[i].split(' ')
class_number = table[0].find('�����') #����� ������� � �������. ����� �������� ������ �������� (� �������� �������, � ���������� � �.�. ��� �����)
status_number = table[0].find('���� ����')
mark_number = table[0].find('�����')
# ��� ��������� ���� �����
# ��������, �� ���� ���������� � try


olymp_name = input("������� �������� ���������")
con = sqlite3.connect('data.db')
cur = con.cursor()
cur.execute('CREATE TABLE ...')
for i in table[1:]:
    cur.execute('INSERT INTO ...')


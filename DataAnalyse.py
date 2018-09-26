#!usr/bin/python3
# DataAnalyse.py

'''
Autor   : Christian Dopatka
Version : 26.09.2018

License:  Creative Commons CC BY-NC
https://creativecommons.org/licenses/?lang=de
'''

import sqlite3

conn = sqlite3.connect("temp.db")
c = conn.cursor()

# Show all Values in the Table 'temperature'
c.execute('SELECT * FROM temperature')
result = c.fetchall()
for r in result:
    print(r)
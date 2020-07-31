# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 15:03:52 2020

@author: ellen
"""


import sqlite3
import codecs

conn = sqlite3.connect('CUNY_map.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM CUNY_location')
fhand = codecs.open('CUNY_map.js', 'w', "utf-8")
fhand.write("myData = [\n")
count = 0
for row in cur :
    lat = row[3]
    lng = row[4]
    name = row[1]
    
 
    print(name, lat, lng)
    print("_____________________")

    count = count + 1
    if count > 1 : fhand.write(",\n")
    output = "["+str(lat)+","+str(lng)+", '"+name+"']"
    fhand.write(output)
 

fhand.write("\n];\n")
cur.close()
fhand.close()

print("ALL DONE!! ")

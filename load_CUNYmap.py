# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 20:03:17 2020

@author: Meilun
"""
import urllib.request
import urllib.parse
import urllib.error
import http
import sqlite3
import json
import ssl


api_key = False

api_key = 'AIzaSyC5Ir9TKJTQqrI33J-c_DKyUFUMq3dePOo'


serviceurl = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"

# Additional detail for urllib
# http.client.HTTPConnection.debuglevel = 1

conn = sqlite3.connect('CUNY_map.sqlite')
cur = conn.cursor()

# SQLite Query
cur.execute('''


CREATE TABLE IF NOT EXISTS CUNY_location (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    address TEXT,
    lat TEXT,
    lng TEXT,
    rating TEXT,
    height TEXT,
    width TEXT,
    html TEXT,
    ref TEXT
);


''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False


ctx.verify_mode = ssl.CERT_NONE


cuny_list = open("cuny.txt")
for line in cuny_list:

    campus_name = line

    parms = dict()
    parms["input"] = campus_name
    parms["inputtype"] = "textquery"
    parms["fields"] = "photos,formatted_address,name,rating,opening_hours,geometry"

    for num in [1, 2, 4]
    print(n)

    if api_key is not False:
        parms['key'] = api_key

    url = serviceurl + urllib.parse.urlencode(parms)
    print(campus_name)
    print('Retrieving', url)

    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    print('==== Retrieve Succeed! ====')

    try:
        js = json.loads(data)
    except:
        print(data)  # We print in case unicode causes an error

    # pull data from JSON and write into SQL
    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS'):
        print('==== Failure To Retrieve ====')
        print(data)


#    print(json.dumps(js, indent=4))

    address = js['candidates'][0]['formatted_address']
    lat = js['candidates'][0]['geometry']['location']['lat']
    lng = js['candidates'][0]['geometry']['location']['lng']
    name = js['candidates'][0]['name']
    photos_height = js['candidates'][0]['photos'][0]['height']
    photos_width = js['candidates'][0]['photos'][0]['width']
    photos_html = js['candidates'][0]['photos'][0]['html_attributions'][0]
    photos_ref = js['candidates'][0]['photos'][0]['photo_reference']
    rating = js['candidates'][0]['rating']

#    print(address, lat,lng)
#    print(name,rating)
#    print(photos_height,photos_width)
#    print(photos_html)
#    print(photos_ref)

    cur.execute('''INSERT INTO CUNY_location (name,address,lat,lng,rating,height,width,html,ref)
                VALUES (?,?,?,?,?,?,?,?,?)''',
                (name, address, lat, lng, rating, photos_height, photos_width, photos_html, photos_ref))

    conn.commit()


print("All Done! ")

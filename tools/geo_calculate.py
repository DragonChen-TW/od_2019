from math import radians, cos, sin, asin, sqrt
#
import requests

def address2geo(address):
    # Note: the key is from web
    parameters = {'address': address, 'key': 'cb649a25c1f81c1451adbeca73623251'}
    url = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(url, parameters)
    response = response.json()
    print('{} 的經緯度：{}'.format(address, response['geocodes'][0]['location']))

    temp = response['geocodes'][0]['location'].split(',')
    lng = float(temp[0])
    lat = float(temp[1])

    return lng, lat

def calculate_distance(lng1, lat1, lng2, lat2):
    # 將十進制度數轉化為弧度
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    # haversine公式
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 地球平均半徑，單位為公里
    return c * r * 1000

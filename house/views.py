from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
import json
import os
import pandas as pd
#
from .models import House
from .auto import get_stat_code
from .automate.Opendata.index_library import search, getHistoryHouseTransInfo
import numpy as np

b = ['住宅大樓(11層含以上有電梯)' '公寓(5樓含以下無電梯)' '透天厝' '套房(1房1廳1衛)'
 '華廈(10層含以下有電梯)']
c = ['The villages and towns urban district' '鼓山區' '苓雅區' '前鎮區' '小港區' '三民區'
 '左營區' '楠梓區' '岡山區' '橋頭區' '鳳山區' '大樹區' '仁武區' '大社區' '阿蓮區' '路竹區' '美濃區' '林園區'
 '大寮區' '鹽埕區' '新興區' '燕巢區' '湖內區' '茄萣區' '鳥松區' '梓官區' '永安區' '旗山區' '內門區' '旗津區'
 '前金區' '彌陀區' '六龜區' '甲仙區' '杉林區']

# Create your views here.
class HouseListView(View):
    def get(self, request):
        houses = list(House.objects.values())

        return JsonResponse(houses, safe=False)
def HouseMapView(request):
    houses = list(House.objects.values())
    # print(houses)

    traffic_fields = ['mrt_score', 'light_rail_score']
    traffic_score = [[int(h[f]) for f in traffic_fields] for h in houses]
    for i, h in enumerate(houses):
        houses[i]['traffic_score'] = sum(traffic_score[i]) / len(traffic_fields)
    print(houses)
    houses_json = json.dumps(houses, ensure_ascii=False)
    # print(houses_json)

    return render(request, 'map.html', {'houses': houses_json})

def ChartView(request):
    house_id = request.GET.get('house_id', 1)
    house = House.objects.get(id=house_id)

    traffic_fields = ['mrt_score', 'light_rail_score']
    traffic_score = [int(house.__dict__[f]) for f in traffic_fields]
    house.traffic_score = sum(traffic_score) / len(traffic_fields)

    fields = [
        'medical_score',
        'freeway_score',
        'traffic_score',
        'police_score',
        'population_score'
    ]
    res = [house.__dict__[f] for f in fields] + [0]

    return render(request, 'chart.html', {'json_data':res})

def searchHouseView(request):
    # if request.GET.get('search_all') and request.GET['search_all']:
    houses = House.objects.all()

    for house in houses:
        res = search(house.lng, house.lat)
        for k in res:
            house.__dict__[k] = res[k]

        house.save()

    return redirect('/house/')

def updateStatView(request):
    for house in House.objects.all():
        if house.stat_code == '':
            res = get_stat_code(house['lng'], house['lat'])
            house['stat_code'] = res['最小']
            house['raw_stat'] = json.dumps(res)

    return redirect('/house/')

class CreateHouseView(View):
    def get(self, request):
        return render(request, 'create_house.html')
    def post(self, request):
        house_d = dict(request.POST)
        # make house
        fields = ['name', 'age', 'address', 'type']
        house = {k: house_d[k][0] for k in fields if house_d.get(k)}
        floats = ['lng', 'lat'  ,'price']
        for f in floats:
            house[f] = float(house_d[f][0])

        # get stat_code
        res = get_stat_code(house['lng'], house['lat'])
        house['stat_code'] = res['最小']
        house['raw_stat'] = json.dumps(res)

        House.objects.create(**house)

        return redirect('/house/')

# rehomes
def aboutView(request):
    return render(request, 'about.html')
def agentView(request):
    return render(request, 'agent.html')
def propertiesView(request, h_id):
    house = House.objects.get(id=h_id)

    if h_id == 1:
        district = '鼓山區'
    else:
        district = '鹽埕區'

    transaction = getHistoryHouseTransInfo(district)
    transaction = [np.log10(t) for t in transaction]
    transaction = json.dumps(transaction)

    return render(request, 'properties.html', {'house': house, 'transaction': transaction})
def comparisonView(request, id1=1, id2=6):
    h1 = House.objects.get(id=id1)
    h2 = House.objects.get(id=id2)

    traffic_fields = ['mrt_score', 'light_rail_score']
    traffic_score = [int(h1.__dict__[f]) for f in traffic_fields]
    h1.traffic_score = sum(traffic_score) / len(traffic_fields)

    traffic_score = [int(h2.__dict__[f]) for f in traffic_fields]
    h2.traffic_score = sum(traffic_score) / len(traffic_fields)

    # dump data
    fields = [
        'medical_score',
        'freeway_score',
        'traffic_score',
        'police_score',
        'population_score'
    ]
    data1 = [h1.__dict__[f] for f in fields]
    data2 = [h2.__dict__[f] for f in fields]

    return render(request, 'comparison.html',
        {'h1': h1, 'h2': h2, 'data1_json': data1, 'data2_json': data2})

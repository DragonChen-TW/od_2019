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
from .automate.Opendata.index_library import search

# Create your views here.
class HouseListView(View):
    def get(self, request):
        houses = list(House.objects.values())

        return JsonResponse(houses, safe=False)
def HouseMapView(request):
    houses = list(House.objects.values())
    houses_json = json.dumps(houses, ensure_ascii=False)
    # print(houses_json)

    return render(request, 'map.html', {'houses': houses_json})

def ChartView(request):
    house_id = request.GET.get('house_id', 1)
    house = House.objects.get(id=house_id)

    fields = ['medical_score', 'freeway_score', 'mrt_score', 'light_rail_score', 'police_score']
    res = [house.__dict__[f] for f in fields] + [0]

    return render(request, 'chart.html', {'json_data':res})

def searchHouseView(request):
    id = request.GET.get('house_id', 1)
    house = House.objects.get(id=id)

    res = search(house.lng, house.lat)
    for k in res:
        house.__dict__[k] = res[k]

    house.save()

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

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

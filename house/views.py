from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
import json
#
from .models import House

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
        # print(house)
        fields = ['name', 'lng', 'lat',  'age', 'price', 'address', 'type']
        house = {k: house_d[k][0] for k in fields if house_d.get(k)}
        floats = ['lng', 'lat'  ,'price']
        for f in floats:
            house[f] = float(house[f])

        if house_d.get('is_near_park'):
            house['is_near_park'] = True
        else:
            house['is_near_park'] = False

        House.objects.create(**house)

        return redirect('/house/')

# class AddStoreView(View):
#     def get(self, request):
#         return render(request, 'add_store.html')
#     def post(self, request):
#         store = request.POST
#         store = dict(store)
#
#         new_id = Store.objects.order_by('-id').first()
#         if not new_id:
#             new_id = 1
#         else:
#             new_id = new_id.id + 1
#
#         Store.objects.get_or_create(id=new_id,
#         name=store['name'][0],address=store['address'][0],
#         phone=store['phone'][0],type=store['type'][0],url=store['url'][0],
#         close_date=store['close_date'][0],open_duration=store['open_duration'][0])
#
#         # Store.objects.get_or_create(**store)
#
#         return redirect('/back/')

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
#
from .models import House

# Create your views here.
class HouseListView(View):
    def get(self, request):
        houses = House.objects.all()
        # stores = [{'':store.id, 'name':store.name} for store in stores]
        json = json.dumps(houses)

        return JsonResponse(houses, safe=False)

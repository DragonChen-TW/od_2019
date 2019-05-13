from django.urls import path
#
from .views import (
    HouseListView, CreateHouseView, HouseMapView,
    searchHouseView, ChartView, updateStatView
)

urlpatterns = [
    path('', HouseMapView),
    path('map/', HouseMapView),
    path('list/', HouseMapView),
    path('search/', searchHouseView),
    path('create/', CreateHouseView.as_view()),
    path('update_stat', updateStatView),
    path('json/', HouseListView.as_view()),
    path('chart/', ChartView),
    # path('calculate/', CalculateView),
]

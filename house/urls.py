from django.urls import path
#
from .views import HouseListView, CreateHouseView, HouseMapView, searchHouseView

urlpatterns = [
    path('', HouseMapView),
    path('map/', HouseMapView),
    path('list/', HouseMapView),
    path('search/', searchHouseView),
    path('create/', CreateHouseView.as_view()),
    path('json/', HouseListView.as_view()),
    # path('calculate/', CalculateView),
]

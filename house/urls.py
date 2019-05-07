from django.urls import path
#
from .views import HouseListView, CreateHouseView, HouseMapView

urlpatterns = [
    path('', HouseMapView),
    path('map/', HouseMapView),
    path('create/', CreateHouseView.as_view()),
    path('json/', HouseListView.as_view()),
    # path('calculate/', CalculateView),
]

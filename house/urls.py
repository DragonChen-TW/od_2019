from django.urls import path
#
from .views import HouseListView, CreateHouseView, HouseMapView, CalculateView

urlpatterns = [
    path('', HouseListView.as_view()),
    path('map/', HouseMapView),
    path('create/', CreateHouseView.as_view()),
    path('calculate/', CalculateView)
]

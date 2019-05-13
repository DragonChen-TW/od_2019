from django.urls import path
#
from .views import (
    HouseListView, CreateHouseView, HouseMapView,
    searchHouseView, ChartView, updateStatView,
    aboutView, agentView, propertiesView
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

    # Rehomes
    path('about/', aboutView),
    path('agent/', agentView),
    path('properties/<int:h_id>/', propertiesView),
]

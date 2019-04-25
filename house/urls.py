from django.urls import path
#
from .views import HouseListView, CreateHouseView

urlpatterns = [
    path('', HouseListView.as_view()),
    path('create/', CreateHouseView.as_view()),
]

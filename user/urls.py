from django.urls import path

from .views import Index, UserRegister, UserSelf, UserLogin, UserLogout

urlpatterns = [
    path('', Index.as_view()),
    path('self/', UserSelf.as_view(), name='self'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('register/', UserRegister.as_view(), name='register'),
]

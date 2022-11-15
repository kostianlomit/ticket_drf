"""drfsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.generics import *
from rest_framework_simplejwt.views import *

from ticket.views import *
from rest_framework import routers

# связывает с ViewSet
# router = routers.DefaultRouter()
# router.register(r'ticket', TicketViewSet)
# print(router.urls)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    # path('api/v1/', include(router.urls)), #  http://127.0.0.1:8000/api/v1/ticket/ для DefaultRouter
    path('api/v1/ticketlist/', TicketAPIList.as_view()), # {'get': 'list'} - для DefaultRout
    path('api/v1/ticket/<int:pk>/', TicketAPIUpdate.as_view()),
    path('api/v1/ticketdestroy/<int:pk>/', TicketDestroy.as_view()), # {'put': 'update'} - для DefaultRout
    path('api/v1/auth/', include('djoser.urls')), # token
    re_path(r'^auth/', include('djoser.urls.authtoken')), # token
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # JWT
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # JWT
    # path('api/v1/token/verify', TokenVerifyView.as_view(), name='token_verify'), # JWT
    path('', manage_items, name="items"),
    path('<slug:key>', manage_item, name="single_item")
]

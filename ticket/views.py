import json

import redis
from django.forms import model_to_dict
from django.shortcuts import render

from rest_framework import generics, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Ticket, Category
from .permitions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializer import TicketSerializer

import psycopg2

class TicketAPIListPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page_size'
    max_page_size = 100

# прописывается для создания Simple/DefaultRouter
# class TicketViewSet(mixins.CreateModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.ListModelMixin,
#                     mixins.RetrieveModelMixin,
#                     mixins.DestroyModelMixin,
#                     GenericViewSet):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#
# # Сокращение данных по индексу [:3]
#     def get_queryset(self):
#         pk = self.kwargs.get("pk")
#
#         if not pk:
#             return Ticket.objects.all()[:3]
#
#         return Ticket.objects.filter(pk=pk)
#
#     @action(methods=['get'], detail=True)
#     def category(self, request,pk=None):
#         cats = Category.objects.get(pk=pk)
#         return Response({'cats': cats.name})

# классы суриализаторов, их функции
import redis

def redis_db(self, request, *args, **kwargs):
    queryset = Ticket.objects.all()
    redis_client = redis.Redis(host="localhost", port=6379, db=0)

    with redis.Redis() as redis_client:
        for k in  redis_client.scan_iter('*', ):
            print(k, redis_client.get(k))


class TicketAPIList(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = TicketAPIListPagination


class TicketAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated, )
    # authentication_classes = (TokenAuthentication, ) # - только по токенам

class TicketDestroy(generics.DestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAdminOrReadOnly,)

class TicketAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


# создание вручную Http запросов
# class TicketAPIView(APIView):
#     def get(self, request):
#         w = Ticket.objects.all()
#         return Response({'posts': TicketSerializer(w, many=True).data})
#
#     def post(self, request):
#         serializer = TicketSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'post ': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         try:
#             instance = Ticket.objects.get(pk=pk)
#
#         except:
#             return Response({"error": "Object does not exists"})
#
#         serializer = TicketSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'post': serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         try:
#             myitem = Ticket.objects.get(pk=pk)
#             myitem.delete()
#
#         except:
#             return Response({"error": "Object does not exists"})
#
#         return Response({"post": "delete post" + str(pk)})



# class TicketAPIView(generics.ListAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer



import json
from django.conf import settings
import redis
from rest_framework.response import Response

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)



@api_view(['GET', 'POST'])
def manage_items(request, *args, **kwargs):
    if request.method == 'GET':
        items = {}
        count = 0
        for key in redis_instance.keys("*"):
            items[key.decode("utf-8")] = redis_instance.get(key)
            count += 1
        response = {
            'count': count,
            'msg': f"Found {count} items.",
            'items': items
        }
        return Response(response, status=200)
    elif request.method == 'POST':
        item = json.loads(request.body)
        key = list(item.keys())[0]
        value = item[key]
        redis_instance.set(key, value)
        response = {
            'msg': f"{key} successfully set to {value}"
        }
        return Response(response, 201)

@api_view(['GET', 'PUT', 'DELETE'])
def manage_item(request, *args, **kwargs):
    if request.method == 'GET':
        if kwargs['key']:
            value = redis_instance.get(kwargs['key'])
            if value:
                response = {
                    'key': kwargs['key'],
                    'value': value,
                    'msg': 'success'
                }
                return Response(response, status=200)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)
    elif request.method == 'PUT':
        if kwargs['key']:
            request_data = json.loads(request.body)
            new_value = request_data['new_value']
            value = redis_instance.get(kwargs['key'])
            if value:
                redis_instance.set(kwargs['key'], new_value)
                response = {
                    'key': kwargs['key'],
                    'value': value,
                    'msg': f"Successfully updated {kwargs['key']}"
                }
                return Response(response, status=200)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)

    elif request.method == 'DELETE':
        if kwargs['key']:
            result = redis_instance.delete(kwargs['key'])
            if result == 1:
                response = {
                    'msg': f"{kwargs['key']} successfully deleted"
                }
                return Response(response, status=404)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)
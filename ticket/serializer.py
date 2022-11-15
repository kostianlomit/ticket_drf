import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = "__all__"


    # Создание собственных сериалазиров
    # title = serializers.CharField(max_length=255)
    # content = serializers.CharField()
    # time_create = serializers.DateTimeField(read_only=True)
    # time_update = serializers.DateTimeField(read_only=True)
    # cat_id = serializers.IntegerField()
    #
    # def create(self, validated_data):
    #     return Ticket.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get("title", instance.title)
    #     instance.content = validated_data.get("content", instance.content)
    #     instance.time_create  = validated_data.get("ttime_create ", instance.time_create)
    #     instance.time_update = validated_data.get("time_update", instance.time_update)
    #     instance.save()
    #     return instance
    #
    # def delete(self, myitem, validated_data):
    #     myitem.title = validated_data.get("title", myitem.title)
    #     myitem.content = validated_data.get("content", myitem.content)
    #     myitem.time_create = validated_data.get("ttime_create ", myitem.time_create)
    #     myitem.time_update = validated_data.get("time_update", myitem.time_update)
    #     myitem.delete()
    #     return myitem

# def encode():
#     model = TicketModel('Number-1', 'Content: info namber-1')
#     model_sr = TicketSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
#
# def decode():
#     stream = io.BytesIO(b'{"title":"Number-1","content":"Content: info namber-1"}')
#     data = JSONParser().parse(stream)
#     serializer = TicketSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)
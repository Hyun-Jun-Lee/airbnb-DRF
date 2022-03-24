from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=140)
    price = serializers.IntegerField()
    bedrooms = serializers.IntegerField()
    instant_book = serializers.BooleanField()
    
class BigRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("__all__")
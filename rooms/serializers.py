from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Room

class ReadRoomSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()
    
    class Meta:
        model = Room
        fields = ("__all__")
        
class WriteRoomSerializer(serializers.Serializer):
    
    name = serializers.CharField(max_length=140)
    address = serializers.CharField(max_length=140)
    price = serializers.IntegerField()
    beds = serializers.IntegerField(default=1)
    lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    check_in = serializers.TimeField(default="00:00:00")
    check_out = serializers.TimeField(default="00:00:00")
    instant_book = serializers.BooleanField(default=False)
    
    def create(self, validated_data):
        return Room.objects.create(**validated_data)
    
    def validate(self,data):
        # instance가 없다는 말은 update가 아니라 create임을 의미
        if not self.instance:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
            if check_in == check_out:
                raise serializers.ValidationError("Check_in & Check_out Error")
        return data
    
    def update(self, instance, validated_data):
        pass
            
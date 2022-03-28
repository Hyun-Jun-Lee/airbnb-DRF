from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Room
from .serializers import RoomSerializer
from rooms import serializers

# Create your views here.

class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    # auth 권한
    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    
class SeeRoomView(RetrieveAPIView):
    
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
 

'''    
class RoomView(APIView):
    
    def get_room(self, pk):
        try:
            room = Room.objects.all(pk=pk)
            return room
        except:
            return None
        
    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = RoomSerializer(room).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # partial=True 특정 field만 업데이트 가능
            serializer = RoomSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(["GET", "POST"])
def rooms_view(request):
    if request.method == "GET":
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True).data
        return Response(serializer)
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(status = status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = RoomSerializer(room).data
            return Response(data=room_serializer,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
'''

@api_view(["GET"])
def room_search(request):
    max_price = request.GET.get("max_price", None)
    min_price = request.GET.get("min_price", None)
    beds = request.GET.get("beds", None)
    bedrooms = request.GET.get("bedrooms", None)
    bathrooms = request.GET.get("bathrooms", None)
    filter_kwargs = {}
    if max_price is not None:
        filter_kwargs["price__lte"] = max_price
    if min_price is not None:
        filter_kwargs["price__gte"] = min_price
    if beds is not None:
        filter_kwargs["beds__gte"] = beds
    if bedrooms is not None:
        filter_kwargs["bedrooms__gte"] = bedrooms
    if bathrooms is not None:
        filter_kwargs["bathrooms__gte"] = bathrooms
    paginator = PageNumberPagination()
    try:
        rooms = Room.objects.filter(**filter_kwargs)
    except ValueError:
        rooms = Room.objects.all()
    results = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)
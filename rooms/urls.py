from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("lists/", views.ListRoomsView.as_view())
]

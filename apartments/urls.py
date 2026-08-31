from django.urls import path
from . import views

urlpatterns = [
    path("", views.apartment_list, name="apartment_list"),
    path("<int:apartment_id>/", views.apartment_detail, name="apartment_detail"),
]


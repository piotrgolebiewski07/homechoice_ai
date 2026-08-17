from django.shortcuts import render
from .models import Apartment


def apartment_list(request):
    apartments = Apartment.objects.all()

    return render(
        request,
        'apartments/apartment_list.html',
        {
            "apartments": apartments,
        }
    )


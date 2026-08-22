from django.shortcuts import render
from .models import Apartment
from django.db.models import F


def apartment_list(request):
    apartments = Apartment.objects.all()

    # Filtering
    selected_city = request.GET.get("city", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    min_area = request.GET.get("min_area", "")
    max_area = request.GET.get("max_area", "")
    rooms_number = request.GET.get("rooms_number", "")
    floor_number = request.GET.get("floor_number", "")

    if selected_city:
        apartments = apartments.filter(city__iexact=selected_city)

    if min_price:
        apartments = apartments.filter(price__gte=min_price)

    if max_price:
        apartments = apartments.filter(price__lte=max_price)

    if min_area:
        apartments = apartments.filter(area__gte=min_area)

    if max_area:
        apartments = apartments.filter(area__lte=max_area)

    if rooms_number:
        if rooms_number == "5_plus":
            apartments = apartments.filter(rooms__gte=5)
        else:
            apartments = apartments.filter(rooms=rooms_number)

    if floor_number:
        if floor_number == "5_plus":
            apartments = apartments.filter(floor__gte=5)
        else:
            apartments = apartments.filter(floor=floor_number)

    apartments = apartments.annotate(price_per_sqm_sort=F("price") / F("area"))

    # Sorting
    sort_by = request.GET.get("sort_by", "newest")
    sort_fields = {
        "city_asc": "city",
        "city_desc": "-city",
        "price_asc": "price",
        "price_desc": "-price",
        "area_asc": "area",
        "area_desc": "-area",
        "room_asc": "rooms",
        "room_desc": "-rooms",
        "floor_asc": "floor",
        "floor_desc": "-floor",
        "newest": "-year_built",
        "oldest": "year_built",
        "price_per_sqm_asc": "price_per_sqm_sort",
        "price_per_sqm_desc": "-price_per_sqm_sort",
    }
    sort_field = sort_fields.get(sort_by, "-year_built")
    apartments = apartments.order_by(sort_field)

    return render(
        request,
        'apartments/apartment_list.html',
        {
            "apartments": apartments,
            "selected_city": selected_city,
            "min_price": min_price,
            "max_price": max_price,
            "min_area": min_area,
            "max_area": max_area,
            "rooms_number": rooms_number,
            "floor_number": floor_number,
            "sort_by": sort_by,
        }
    )


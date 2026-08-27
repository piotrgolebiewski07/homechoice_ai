from django.shortcuts import render
from .models import Apartment
from django.db.models import F
from django.core.paginator import Paginator

PAGE_SIZE_OPTIONS = (10, 20, 50)


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

    per_page = request.GET.get("per_page", "10")
    try:
        per_page = int(per_page)
    except (TypeError, ValueError):
        per_page = 10

    if per_page not in PAGE_SIZE_OPTIONS:
        per_page = 10

    paginator = Paginator(apartments, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(
        number=page_obj.number,
        on_each_side=1,
        on_ends=1,
    )

    query_params = request.GET.copy()
    query_params.pop("page", None)
    query_string = query_params.urlencode()

    page_size_params = request.GET.copy()
    page_size_params.pop("page", None)
    page_size_params.pop("per_page", None)
    page_size_query_string = page_size_params.urlencode()

    return render(
        request,
        'apartments/apartment_list.html',
        {
            "apartments": page_obj,
            "selected_city": selected_city,
            "min_price": min_price,
            "max_price": max_price,
            "min_area": min_area,
            "max_area": max_area,
            "rooms_number": rooms_number,
            "floor_number": floor_number,
            "sort_by": sort_by,
            "page_obj": page_obj,
            "query_string": query_string,
            "page_range": page_range,
            "per_page": per_page,
            "per_page": per_page,
            "page_size_options": PAGE_SIZE_OPTIONS,
            "page_size_query_string": page_size_query_string,
        }
    )


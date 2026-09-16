from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Apartment


class ApartmentModelTests(TestCase):
    def setUp(self):
        self.apartment = Apartment(
            city="Warszawa",
            price=Decimal("600000.00"),
            area=Decimal("60.00"),
            rooms=3,
        )

    def test_price_per_sqm(self):
        self.assertEqual(
            self.apartment.price_per_sqm,
            Decimal("10000"),
        )

    def test_price_per_sqm_returns_none_when_area_is_zero(self):
        self.apartment.area = Decimal("0.00")

        self.assertIsNone(self.apartment.price_per_sqm)

    def test_string_representation(self):
        self.assertEqual(
            str(self.apartment),
            "Warszawa - 60.00 m² - 600000.00 zł",
        )


class ApartmentDetailViewTests(TestCase):
    def setUp(self):
        self.apartment = Apartment.objects.create(
            city="Warszawa",
            price=Decimal("600000.00"),
            area=Decimal("60.00"),
            rooms=3,
            price_difference_pct=Decimal("15.00"),
        )

    def test_detail_view_returns_success(self):
        response = self.client.get(
            reverse("apartment_detail", args=[self.apartment.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "apartments/apartment_detail.html",
        )
        self.assertEqual(
            response.context["apartment"],
            self.apartment,
        )

    def test_detail_view_returns_404_for_missing_apartment(self):
        response = self.client.get(
            reverse("apartment_detail", args=[999999])
        )

        self.assertEqual(response.status_code, 404)

    def test_detail_view_calculates_marker_position(self):
        response = self.client.get(
            reverse("apartment_detail", args=[self.apartment.pk])
        )

        self.assertEqual(response.context["marker_position"], 75)

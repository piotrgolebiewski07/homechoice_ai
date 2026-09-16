from decimal import Decimal

from django.test import TestCase

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

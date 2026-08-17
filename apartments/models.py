from django.db import models


class Apartment(models.Model):
    MARKET_CHOICES = [
        ("primary", "Pierwotny"),
        ("secondary", "Wtórny"),
    ]

    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    area = models.DecimalField(max_digits=6, decimal_places=2)
    rooms = models.PositiveSmallIntegerField()
    floor = models.PositiveSmallIntegerField()
    year_built = models.PositiveSmallIntegerField()
    market_type = models.CharField(max_length=20, choices=MARKET_CHOICES)

    def __str__(self):
        return f"{self.city} - {self.district} ({self.area}) m² - {self.price}"


from django.db import models


class Apartment(models.Model):
    MARKET_CHOICES = [
        ("primary", "Pierwotny"),
        ("secondary", "Wtórny"),
        ("unknown", "Brak danych"),
    ]

    city = models.CharField(max_length=100)
    source_id = models.CharField(
        max_length=32,
        unique=True,
        null=True,
        blank=True,
    )
    district = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    area = models.DecimalField(max_digits=6, decimal_places=2)
    rooms = models.PositiveSmallIntegerField()
    floor = models.PositiveSmallIntegerField()
    year_built = models.PositiveSmallIntegerField(null=True, blank=True)
    market_type = models.CharField(max_length=20, choices=MARKET_CHOICES,)

    @property
    def price_per_sqm(self):
        if not self.area:
            return None

        return self.price / self.area

    def __str__(self):
        return f"{self.city} - {self.district} ({self.area}) m² - {self.price}"


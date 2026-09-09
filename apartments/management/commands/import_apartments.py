import csv
from pathlib import Path
from decimal import Decimal

from django.core.management.base import BaseCommand
from apartments.models import Apartment


def parse_optional_int(value):
    if value == "":
        return None
    return int(value)


def parse_optional_bool(value):
    if value == "True":
        return True

    if value == "False":
        return False

    return None


def parse_decimal(value):
    return Decimal(value).quantize(Decimal("0.01"))


class Command(BaseCommand):
    help = "Imports apartment offers from a CSV file"

    def handle(self, *args, **options):
        file_path = Path("data/processed/apartments_cleaned.csv")

        with file_path.open(encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            created_count = 0
            updated_count = 0

            for row in reader:
                apartment_data = {
                    "source_id": row["source_id"],
                    "city": row["city"],
                    "district": "",
                    "price": parse_decimal(row["price"]),
                    "area": parse_decimal(row["area"]),
                    "rooms": int(row["rooms"]),
                    "floor": parse_optional_int(row["floor"]),
                    "floor_count": parse_optional_int(row["floor_count"]),
                    "year_built": parse_optional_int(row["year_built"]),
                    "market_type": "",
                    "has_parking": parse_optional_bool(row["has_parking"]),
                    "has_balcony": parse_optional_bool(row["has_balcony"]),
                    "has_elevator": parse_optional_bool(row["has_elevator"]),
                    "city_median_price_per_sqm": parse_decimal(row["city_median_price_per_sqm"]),
                    "price_difference_pct": parse_decimal(row["price_difference_pct"]),
                    "price_rating": row["price_rating"],
                }
                apartment = Apartment(**apartment_data)
                apartment.full_clean(validate_unique=False)

                apartment, created = Apartment.objects.update_or_create(
                    source_id=apartment_data["source_id"],
                    defaults=apartment_data,
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        message = f"Import zakończony. Dodano {created_count}, zaktualizowano: {updated_count}."
        self.stdout.write(message)
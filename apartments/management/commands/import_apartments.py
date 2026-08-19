import csv
from pathlib import Path
from decimal import Decimal
from itertools import islice

from django.core.management.base import BaseCommand
from apartments.models import Apartment


class Command(BaseCommand):
    help = "Imports apartment offers from a CSV file"

    def handle(self, *args, **options):
        file_path = Path("data/raw/apartments_pl_2023_08.csv")

        with file_path.open(encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            created_count = 0
            existing_count = 0

            for row in islice(reader, 10):
                apartment_data = {
                    "city": row["city"].title(),
                    "source_id": row["id"],
                    "district": "",
                    "price": Decimal(row["price"]),
                    "area": Decimal(row["squareMeters"]),
                    "rooms": int(float(row["rooms"])),
                    "floor": int(float(row["floor"])),
                    "year_built": (
                        int(float(row["buildYear"]))
                        if row["buildYear"]
                        else None
                    ),
                    "market_type": "unknown",
                }
                apartment = Apartment(**apartment_data)
                apartment.full_clean(validate_unique=False)

                apartment, created = Apartment.objects.get_or_create(
                    source_id=apartment_data["source_id"],
                    defaults=apartment_data,
                )

                if created:
                    created_count += 1
                else:
                    existing_count += 1

        message = f"Testowy import zakończony. Dodano {created_count}, istniejące: {existing_count}."
        self.stdout.write(message)
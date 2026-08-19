import csv
from pathlib import Path
from decimal import Decimal

from django.core.management.base import BaseCommand
from apartments.models import Apartment


class Command(BaseCommand):
    help = "Imports apartment offers from a CSV file"

    def handle(self, *args, **options):
        file_path = Path("data/raw/apartments_pl_2023_08.csv")

        with file_path.open(encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            headers = reader.fieldnames
            first_row = next(reader)
            apartment_data = {
                "city": first_row["city"].title(),
                "source_id": first_row["id"],
                "district": "",
                "price": Decimal(first_row["price"]),
                "area": Decimal(first_row["squareMeters"]),
                "rooms": int(float(first_row["rooms"])),
                "floor": int(float(first_row["floor"])),
                "year_built": (
                    int(float(first_row["buildYear"]))
                    if first_row["buildYear"]
                    else None
                ),
                "market_type": "unknown",
            }
            apartment = Apartment(**apartment_data)
            apartment.full_clean()

        self.stdout.write(f"Kolumny: {headers}")
        self.stdout.write(f"Przygotowany rekord: {apartment_data}")
        self.stdout.write(
            self.style.SUCCESS("Rekord przeszedł walidację modelu.")
        )
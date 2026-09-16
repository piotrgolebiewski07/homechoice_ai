# HomeChoice AI

HomeChoice AI is a Django web application for browsing and analyzing apartment listings in Poland.

The current version uses statistical price analysis to compare each apartment's price per square meter with the median price in its city. A machine learning valuation model is planned for a future version.

## Features

- Browse apartment listings
- Filter by city, price, area, room count, and floor
- Sort listings by price, area, city, floor, year, and price per square meter
- Paginated apartment list
- Configurable number of results per page
- Apartment detail view
- Price-per-square-meter calculation
- Comparison with the city median
- Rule-based apartment price rating
- CSV data import using a Django management command
- Data cleaning and exploration with Pandas

## Technology

- Python
- Django 6.1
- SQLite
- Pandas
- HTML
- CSS

## Data pipeline

```text
Raw apartment dataset
        ↓
Pandas data exploration and cleaning
        ↓
Processed CSV file
        ↓
Django management command
        ↓
Application database
```

The data preparation process is available in:

```text
notebooks/01_data_exploration.ipynb
```

The processed dataset is imported using:

```text
apartments/management/commands/import_apartments.py
```

## Run locally

1. Clone the repository:

```bash
git clone https://github.com/piotrgolebiewski07/homechoice_ai.git
cd homechoice_ai
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Import apartment data:

```bash
python manage.py import_apartments
```

6. Start the development server:

```bash
python manage.py runserver
```

7. Open the application:

```text
http://127.0.0.1:8000/apartments/
```

## Environment variables

The application supports the following environment variables:

```text
DJANGO_SECRET_KEY
DJANGO_DEBUG
DJANGO_ALLOWED_HOSTS
```

Default values are provided for local development. Production deployment should use a unique secret key and disable debug mode.

## Project status

The project is under active development. Planned features include apartment comparison, reports, responsive mobile layouts, automated tests, and a machine learning valuation model.

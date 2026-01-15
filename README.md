# Address Book API

A RESTful API built with FastAPI for managing addresses with geographic coordinates.

The API supports full CRUD operations.

## Features

- Create addresses with street, city, country, and GPS coordinates
- Read single address or list all with pagination
- Update addresses (partial updates supported)
- Delete addresses from the database
- Search addresses within a given distance from coordinates (incomplete)
- Validation using Pydantic models
- SQLite database for data persistence
- Interactive API documentation (Swagger UI & ReDoc)

## Project Structure

```
address_book_repo/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py               # FastAPI application entry point
│   ├── database.py           # Database configuration & session
│   ├── models.py             # SQLAlchemy ORM models
│   ├── schemas.py            # Pydantic validation schemas
│   ├── crud.py               # Database CRUD operations
│   ├── routers/
│   │   ├── __init__.py
│   │   └── addresses.py      # Address API endpoints
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .gitignore               # Git ignore rules
```

API available at: http://localhost:8000

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Navigate to the Project

```bash
cd /home/anjali/Documents/courses/fastapi/address_book_repo
```

## First Time Setup

```bash
# 1. Navigate to project
cd address_book_application

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the server
uvicorn app.main:app --reload --port 8000
```

## API Documentation

Once the server is running, access the interactive documentation:

| Documentation | URL |
|--------------|-----|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

## API Endpoints

### Root Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API welcome message and info |
| GET | `/health` | Health check endpoint |

### Address Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/addresses/` | Create a new address |
| GET | `/addresses/` | List all addresses |
| GET | `/addresses/{id}` | Get address by ID |
| PUT | `/addresses/{id}` | Update an address |
| DELETE | `/addresses/{id}` | Delete an address |
| GET | `/addresses/search/nearby` | Find nearby addresses |

## Usage Examples

### Create Address

```bash
curl -X POST "http://localhost:8000/addresses/" \
  -H "Content-Type: application/json" \
  -d '{
    "street": "123 Main Street",
    "city": "Indore",
    "state": "MP",
    "country": "India",
    "postal_code": "452006",
    "latitude": 22.7196,
    "longitude": 75.8577
  }'
```

### Get All Addresses

```bash
curl http://localhost:8000/addresses/
```

### Find Nearby Addresses

```bash
curl "http://localhost:8000/addresses/search/nearby?latitude=22.7196&longitude=75.8577&distance_km=50"
```

## Dependencies

| Package | Purpose |
|---------|---------|
| FastAPI | Web framework |
| Uvicorn | ASGI server |
| SQLAlchemy | Database ORM |
| Pydantic | Data validation |
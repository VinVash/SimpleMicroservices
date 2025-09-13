# Academic Financial Management API - Cloud Computing Assignment

## Overview

This project implements an "API first" microservices architecture using FastAPI for managing academic financial data at Columbia University. The system provides RESTful APIs for managing persons, addresses, tuition records, and scholarships with auto-generated OpenAPI documentation.

## Assignment Requirements Fulfilled

### ✅ Implemented Resources
- **Tuition** - Academic fee and tuition management *(New Resource)*
- **Scholarship** - Financial aid and scholarship tracking *(New Resource)*
- **Person** and **Address** models were already present in the template repository.

### ✅ API Endpoints Implemented
For each resource, the following RESTful endpoints are implemented as per Sprint Goal:

#### Tuition Resource (`/tuitions`)
- `GET /tuitions` - List all tuition records with filtering
- `POST /tuitions` - Create a new tuition record
- `GET /tuitions/{id}` - Get specific tuition record by ID
- `PUT /tuitions/{id}` - Replace entire tuition record
- `DELETE /tuitions/{id}` - Delete tuition record

#### Scholarship Resource (`/scholarships`)
- `GET /scholarships` - List all scholarships with filtering
- `POST /scholarships` - Create a new scholarship
- `GET /scholarships/{id}` - Get specific scholarship by ID
- `PUT /scholarships/{id}` - Replace entire scholarship record
- `DELETE /scholarships/{id}` - Delete scholarship

### ✅ Additional Features
- **PATCH** endpoints for partial updates on all resources



## Project Structure

```
SimpleMicroservices/
├── main.py                 # FastAPI application with all endpoints
├── requirements.txt        # Python dependencies
├── models/                 # Pydantic data models
│   ├── person.py          # Person model (Old)
│   ├── address.py         # Address model (Old)
│   ├── tuition.py         # Tuition model (New)
│   ├── scholarship.py     # Scholarship model (New)
│   └── health.py          # Health check model (Old)
├── framework/             # Framework components
├── middleware/            # Middleware components
├── resources/             # Resource handlers
├── services/              # Business logic services
└── utils/                 # Utility functions
```

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd SimpleMicroservices
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Start the server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API Base URL:** http://localhost:8000
- **Open API Documentation (Swagger UI):** http://localhost:8000/docs

## API Documentation
The application automatically generates OpenAPI documentation accessible using:

### Swagger UI (Recommended)
Visit http://localhost:8000/docs for an interactive interface where you can:
- Explore all available endpoints
- Test API calls directly in the browser
- View request/response schemas
- See example payloads


## Environment Configuration
The application supports environment-based configuration:
- `FASTAPIPORT` - Server port (default: 8000)

## Data Storage
Currently uses in-memory "fake" database for data storage, making it perfect for development and testing. Data is reset when the application restarts.

## Assignment Validation

This implementation satisfies all assignment requirements:
- ✅ Two new resources (Tuition, Scholarship) implemented as microservices
- ✅ All required HTTP methods (GET, POST, PUT, DELETE) implemented
- ✅ Complete OpenAPI annotations for auto-generated documentation  
- ✅ Tested endpoints accessible via interactive documentation
- ✅ "API first" approach

---

**Course:** Cloud Computing (COMS4153)
**Student:** Vinamra Vashishth  
**UNI:** VV2418
**Implementation Date:** 13 September 2025

from __future__ import annotations

import os
import socket
from datetime import datetime, timezone

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.tuition import TuitionCreate, TuitionRead, TuitionUpdate
from models.scholarship import ScholarshipCreate, ScholarshipRead, ScholarshipUpdate
from models.health import Health

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
tuitions: Dict[UUID, TuitionRead] = {}
scholarships: Dict[UUID, ScholarshipRead] = {}

app = FastAPI(
    title="Academic Financial Management API",
    description="Demo FastAPI app using Pydantic v2 models for Person, Address, Tuition, and Scholarship",
    version="0.2.0",
)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.now(timezone.utc).isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]

@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(addresses.values())

    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]

    return results

@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]

@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]

# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------
@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    # Each person gets its own UUID; stored as PersonRead
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read

@app.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    results = list(persons.values())

    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]

    # nested address filtering
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]

    return results

@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]

@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]

# -----------------------------------------------------------------------------
# Tuition endpoints
# -----------------------------------------------------------------------------
@app.post("/tuitions", response_model=TuitionRead, status_code=201)
def create_tuition(tuition: TuitionCreate):
    tuition_read = TuitionRead(**tuition.model_dump())
    tuitions[tuition_read.id] = tuition_read
    return tuition_read

@app.get("/tuitions", response_model=List[TuitionRead])
def list_tuitions(
    student_uni: Optional[str] = Query(None, description="Filter by student UNI"),
    tuition_type: Optional[str] = Query(None, description="Filter by tuition type"),
    semester: Optional[str] = Query(None, description="Filter by semester"),
    year: Optional[int] = Query(None, description="Filter by academic year"),
):
    results = list(tuitions.values())

    if student_uni is not None:
        results = [t for t in results if t.student_uni == student_uni]
    if tuition_type is not None:
        results = [t for t in results if t.tuition_type == tuition_type]
    if semester is not None:
        results = [t for t in results if t.semester == semester]
    if year is not None:
        results = [t for t in results if t.year == year]

    return results

@app.get("/tuitions/{tuition_id}", response_model=TuitionRead)
def get_tuition(tuition_id: UUID):
    if tuition_id not in tuitions:
        raise HTTPException(status_code=404, detail="Tuition record not found")
    return tuitions[tuition_id]

@app.patch("/tuitions/{tuition_id}", response_model=TuitionRead)
def update_tuition(tuition_id: UUID, update: TuitionUpdate):
    if tuition_id not in tuitions:
        raise HTTPException(status_code=404, detail="Tuition record not found")
    stored = tuitions[tuition_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    tuitions[tuition_id] = TuitionRead(**stored)
    return tuitions[tuition_id]

@app.put("/tuitions/{tuition_id}", response_model=TuitionRead)
def replace_tuition(tuition_id: UUID, tuition: TuitionCreate):
    if tuition_id not in tuitions:
        raise HTTPException(status_code=404, detail="Tuition record not found")
    # Keep the original id and timestamps, replace everything else
    original = tuitions[tuition_id]
    tuition_data = tuition.model_dump()
    tuition_data["id"] = original.id
    tuition_data["created_at"] = original.created_at
    tuition_data["updated_at"] = datetime.now(timezone.utc)
    tuitions[tuition_id] = TuitionRead(**tuition_data)
    return tuitions[tuition_id]

@app.delete("/tuitions/{tuition_id}")
def delete_tuition(tuition_id: UUID):
    if tuition_id not in tuitions:
        raise HTTPException(status_code=404, detail="Tuition record not found")
    del tuitions[tuition_id]
    return {"message": "Tuition record deleted successfully"}

# -----------------------------------------------------------------------------
# Scholarship endpoints
# -----------------------------------------------------------------------------
@app.post("/scholarships", response_model=ScholarshipRead, status_code=201)
def create_scholarship(scholarship: ScholarshipCreate):
    scholarship_read = ScholarshipRead(**scholarship.model_dump())
    scholarships[scholarship_read.id] = scholarship_read
    return scholarship_read

@app.get("/scholarships", response_model=List[ScholarshipRead])
def list_scholarships(
    scholarship_type: Optional[str] = Query(None, description="Filter by scholarship type"),
    sponsor_organization: Optional[str] = Query(None, description="Filter by sponsor organization (partial match)"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
):
    results = list(scholarships.values())

    if scholarship_type is not None:
        results = [s for s in results if s.scholarship_type == scholarship_type]
    if sponsor_organization is not None:
        results = [s for s in results if sponsor_organization.lower() in s.sponsor_organization.lower()]
    if is_active is not None:
        results = [s for s in results if s.is_active == is_active]

    return results

@app.get("/scholarships/{scholarship_id}", response_model=ScholarshipRead)
def get_scholarship(scholarship_id: UUID):
    if scholarship_id not in scholarships:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return scholarships[scholarship_id]

@app.patch("/scholarships/{scholarship_id}", response_model=ScholarshipRead)
def update_scholarship(scholarship_id: UUID, update: ScholarshipUpdate):
    if scholarship_id not in scholarships:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    stored = scholarships[scholarship_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    scholarships[scholarship_id] = ScholarshipRead(**stored)
    return scholarships[scholarship_id]

@app.put("/scholarships/{scholarship_id}", response_model=ScholarshipRead)
def replace_scholarship(scholarship_id: UUID, scholarship: ScholarshipCreate):
    if scholarship_id not in scholarships:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    # Keep the original id and timestamps, replace everything else
    original = scholarships[scholarship_id]
    scholarship_data = scholarship.model_dump()
    scholarship_data["id"] = original.id
    scholarship_data["created_at"] = original.created_at
    scholarship_data["updated_at"] = datetime.now(timezone.utc)
    scholarships[scholarship_id] = ScholarshipRead(**scholarship_data)
    return scholarships[scholarship_id]

@app.delete("/scholarships/{scholarship_id}")
def delete_scholarship(scholarship_id: UUID):
    if scholarship_id not in scholarships:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    del scholarships[scholarship_id]
    return {"message": "Scholarship deleted successfully"}


# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Welcome to the Person/Address/Tuition/Scholarship API. See /docs for OpenAPI UI.",
    }

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

# routes/country_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from helpers.database import get_db
from helpers.auth import get_current_user
from models import Country
from schemas import CountryCreate, CountryUpdate

router = APIRouter()


@router.get("/countries")
def get_countries(db: Session = Depends(get_db)):
    countries = db.query(Country).all()
    return countries


@router.post("/countries")
def create_country(
    country: CountryCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    new_country = Country(**country.dict())
    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country


# Add other CRUD operations as needed
@router.get("/countries/{country_id}")
def get_country(country_id: int, db: Session = Depends(get_db)):
    countries = get_countries(db)
    country = next((c for c in countries if c.id_country == country_id), None)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@router.put("/countries/{country_id}")
def update_country(
    country_id: int,
    country: CountryUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_country = db.query(Country).filter(Country.id_country == country_id).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    for key, value in country.dict(exclude_unset=True).items():
        setattr(db_country, key, value)
    db.commit()
    db.refresh(db_country)
    return db_country


@router.delete("/countries/{country_id}")
def delete_country(
    country_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    country = db.query(Country).filter(Country.id_country == country_id).first()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    db.delete(country)
    db.commit()
    return {"message": "Country deleted successfully"}

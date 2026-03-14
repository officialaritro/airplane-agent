from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from app.database import get_db
from models.models import User, FlightPreference, MonitoredFlight, Disruption, Claim


router = APIRouter()


class UserCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class FlightPreferenceCreate(BaseModel):
    loyalty_program: Optional[str] = None
    seat_preference: Optional[str] = None
    alliance: Optional[str] = None
    max_connections: int = 1


class FlightPreferenceResponse(BaseModel):
    user_id: str
    loyalty_program: Optional[str]
    seat_preference: Optional[str]
    alliance: Optional[str]
    max_connections: int

    class Config:
        from_attributes = True


class MonitoredFlightCreate(BaseModel):
    flight_no: str
    icao24: Optional[str] = None
    dep_airport: str
    arr_airport: str
    scheduled_dep: datetime


class MonitoredFlightResponse(BaseModel):
    id: str
    user_id: str
    flight_no: str
    icao24: Optional[str]
    dep_airport: str
    arr_airport: str
    scheduled_dep: datetime
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DisruptionResponse(BaseModel):
    id: str
    flight_id: str
    type: str
    delay_minutes: Optional[int]
    cause: Optional[str]
    detected_at: datetime

    class Config:
        from_attributes = True


class ClaimResponse(BaseModel):
    id: str
    disruption_id: Optional[str]
    user_id: str
    carrier: str
    regulation: str
    amount_eur: Optional[float]
    status: str
    submitted_at: Optional[datetime]
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True


@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(email=user.email, name=user.name)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users/{user_id}/preferences", response_model=FlightPreferenceResponse)
async def create_preferences(
    user_id: str, prefs: FlightPreferenceCreate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_prefs = FlightPreference(
        user_id=user_id,
        loyalty_program=prefs.loyalty_program,
        seat_preference=prefs.seat_preference,
        alliance=prefs.alliance,
        max_connections=prefs.max_connections,
    )
    db.add(db_prefs)
    await db.commit()
    await db.refresh(db_prefs)
    return db_prefs


@router.post("/users/{user_id}/flights", response_model=MonitoredFlightResponse)
async def add_flight(
    user_id: str, flight: MonitoredFlightCreate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_flight = MonitoredFlight(
        user_id=user_id,
        flight_no=flight.flight_no,
        icao24=flight.icao24,
        dep_airport=flight.dep_airport,
        arr_airport=flight.arr_airport,
        scheduled_dep=flight.scheduled_dep,
    )
    db.add(db_flight)
    await db.commit()
    await db.refresh(db_flight)
    return db_flight


@router.get("/users/{user_id}/flights", response_model=list[MonitoredFlightResponse])
async def get_flights(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MonitoredFlight).where(MonitoredFlight.user_id == user_id)
    )
    return result.scalars().all()


@router.get("/users/{user_id}/disruptions", response_model=list[DisruptionResponse])
async def get_disruptions(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Disruption)
        .join(MonitoredFlight)
        .where(MonitoredFlight.user_id == user_id)
        .order_by(Disruption.detected_at.desc())
    )
    return result.scalars().all()


@router.get("/users/{user_id}/claims", response_model=list[ClaimResponse])
async def get_claims(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Claim)
        .where(Claim.user_id == user_id)
        .order_by(Claim.submitted_at.desc())
    )
    return result.scalars().all()


@router.get("/health")
async def health_check():
    return {"status": "healthy"}

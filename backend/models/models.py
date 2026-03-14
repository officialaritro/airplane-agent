from sqlalchemy import (
    Column,
    String,
    DateTime,
    Text,
    Integer,
    Numeric,
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(Text, unique=True, nullable=False)
    name = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    flight_preferences = relationship(
        "FlightPreference", back_populates="user", uselist=False
    )
    monitored_flights = relationship("MonitoredFlight", back_populates="user")
    claims = relationship("Claim", back_populates="user")


class FlightPreference(Base):
    __tablename__ = "flight_preferences"

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    loyalty_program = Column(String(100))
    seat_preference = Column(String(20))
    alliance = Column(String(20))
    max_connections = Column(Integer, default=1)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user = relationship("User", back_populates="flight_preferences")


class MonitoredFlight(Base):
    __tablename__ = "monitored_flights"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    flight_no = Column(String(20), nullable=False)
    icao24 = Column(String(10))
    dep_airport = Column(String(4), nullable=False)
    arr_airport = Column(String(4), nullable=False)
    scheduled_dep = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), default="SCHEDULED")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="monitored_flights")
    disruptions = relationship("Disruption", back_populates="flight")

    __table_args__ = (Index("ix_monitored_flights_user_status", "user_id", "status"),)


class Disruption(Base):
    __tablename__ = "disruptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flight_id = Column(
        UUID(as_uuid=True),
        ForeignKey("monitored_flights.id", ondelete="CASCADE"),
        nullable=False,
    )
    type = Column(String(20), nullable=False)
    delay_minutes = Column(Integer)
    cause = Column(String(50))
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    raw_state = Column(JSONB)

    flight = relationship("MonitoredFlight", back_populates="disruptions")
    claims = relationship("Claim", back_populates="disruption")


class Claim(Base):
    __tablename__ = "claims"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    disruption_id = Column(
        UUID(as_uuid=True), ForeignKey("disruptions.id", ondelete="CASCADE")
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    carrier = Column(String(2), nullable=False)
    regulation = Column(String(10), nullable=False)
    amount_eur = Column(Numeric(8, 2))
    status = Column(String(20), default="DRAFT")
    submitted_at = Column(DateTime(timezone=True))
    resolved_at = Column(DateTime(timezone=True))
    outcome_notes = Column(JSONB)
    doc_url = Column(Text)

    user = relationship("User", back_populates="claims")
    disruption = relationship("Disruption", back_populates="claims")

    __table_args__ = (
        Index("ix_claims_user_status", "user_id", "status"),
        Index("ix_claims_carrier_status", "carrier", "status"),
    )


class CarrierRule(Base):
    __tablename__ = "carrier_rules"

    carrier_iata = Column(String(2), primary_key=True)
    regulation = Column(String(10), nullable=False)
    rules = Column(JSONB, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

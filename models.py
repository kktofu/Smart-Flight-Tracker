from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy import Integer, String, Float,ForeignKey

class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)

class FlightForm(db.Model):
    __tablename__ = "flights_form"
    id: Mapped[int] = mapped_column(primary_key=True)
    From: Mapped[str] = mapped_column(String(100))
    To: Mapped[str] = mapped_column(String(100))
    Date: Mapped[str] = mapped_column(String(100))
    Class_name: Mapped[str] = mapped_column(String(100))
    go_last_lowest_price: Mapped[int] = mapped_column(Integer, nullable=True)
    back_last_lowest_price: Mapped[int] = mapped_column(Integer, nullable=True)
    Email: Mapped[str] = mapped_column(String(100))

    tickets = relationship("Ticket", back_populates="flight")

class Ticket(db.Model):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flight_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("flights_form.id"))
    direction: Mapped[str] = mapped_column(String(20))
    flight_no: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)
    depart_time: Mapped[str] = mapped_column(String(100))
    arrive_time: Mapped[str] = mapped_column(String(100))
    duration: Mapped[str] = mapped_column(String(100))

    flight = relationship("FlightForm", back_populates="tickets")
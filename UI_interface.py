from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy import Integer, String, Float,ForeignKey
from forms import CreateFlightForm
from scraping import FlightScraper

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "my_super_secret_key"

class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

class FlightForm(db.Model):
    __tablename__ = "flights_form"
    id: Mapped[int] = mapped_column(primary_key=True)
    From: Mapped[str] = mapped_column(String(100))
    To: Mapped[str] = mapped_column(String(100))
    Date: Mapped[str] = mapped_column(String(100))
    Class_name: Mapped[str] = mapped_column(String(100))
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

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    form = CreateFlightForm()
    if form.validate_on_submit():
        flight_form = FlightForm(
            From=form.From.data,
            To=form.To.data,
            Date=form.Date.data,
            Class_name=form.Class_name.data,
            Email=form.Email.data
        )
        db.session.add(flight_form)
        db.session.commit()

        scraper = FlightScraper()
        departure_price,destination_price = scraper.run_selenium_price_scraper(
            From=flight_form.From,
            To=flight_form.To,
            Date=flight_form.Date,
            Class_name=flight_form.Class_name.split(",")[1],
            class_level=flight_form.Class_name.split(",")[0]
        )

        for data in departure_price:
            ticket = Ticket(
            flight_id=flight_form.id,
            direction="departure",
            flight_no= data["flight_no"],
            price=data["price"],
            depart_time=data["depart_time"],
            arrive_time=data["arrive_time"],
            duration=data["duration"]
            )
            db.session.add(ticket)

        for item in destination_price:
            ticket = Ticket(
                flight_id=flight_form.id,
                direction="return",
                flight_no=item["flight_no"],
                price=item["price"],
                depart_time=item["depart_time"],
                arrive_time=item["arrive_time"],
                duration=item["duration"]
            )
            db.session.add(ticket)
        db.session.commit()

        return redirect(url_for('record'))
    return render_template("index.html",form=form)

@app.route('/record')
def record():
    tickets = db.session.execute(db.select(Ticket)).scalars().all()
    return render_template("record.html",tickets=tickets)

@app.route("/delete/<int:flight_id>")
def delete_ticket(flight_id):
    post_to_delete = db.get_or_404(Ticket, flight_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('record'))


if __name__ == "__main__":
    app.run(debug=True)
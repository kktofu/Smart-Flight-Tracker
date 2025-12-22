from flask import Flask,render_template,request,redirect,url_for
from models import db, FlightForm, Ticket
from flask_apscheduler import APScheduler
from forms import CreateFlightForm
from scraping import FlightScraper
from jobs import daily_flight_check
import datetime
import os

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "my_super_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

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


scheduler = APScheduler()


if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    scheduler.init_app(app)
    scheduler.start()

    scheduler.add_job(
        id="daily_flight_check",
        func=daily_flight_check,
        args=[app],
        trigger="cron",
        hour=18,
        minute=45
    )


if __name__ == "__main__":
    app.run(debug=True)
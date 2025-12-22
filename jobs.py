from models import db, FlightForm, Ticket
from scraping import FlightScraper
def daily_flight_check(app):
    with app.app_context():
        flights = FlightForm.query.all()
        scraper = FlightScraper()

        for flight in flights:
            departure, destination = scraper.run_selenium_price_scraper(
                From=flight.From,
                To=flight.To,
                Date=flight.Date,
                Class_name=flight.Class_name.split(",")[1],
                class_level=flight.Class_name.split(",")[0]
            )
            for data in departure:
                ticket = Ticket(
                    flight_id=flight.id,
                    direction="departure",
                    flight_no=data["flight_no"],
                    price=data["price"],
                    depart_time=data["depart_time"],
                    arrive_time=data["arrive_time"],
                    duration=data["duration"]
                )
                db.session.add(ticket)

            for item in destination:
                ticket = Ticket(
                    flight_id=flight.id,
                    direction="return",
                    flight_no=item["flight_no"],
                    price=item["price"],
                    depart_time=item["depart_time"],
                    arrive_time=item["arrive_time"],
                    duration=item["duration"]
                )
                db.session.add(ticket)
        db.session.commit()



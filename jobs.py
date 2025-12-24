from models import db, FlightForm, Ticket
from scraping import FlightScraper
from mailer import send_price_alert
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

            today_go_lowest = min(d["price"] for d in departure)
            today_back_lowest = min(d["price"] for d in destination)

            if flight.go_last_lowest_price is None:

                flight.go_last_lowest_price = today_go_lowest

            elif today_go_lowest < flight.go_last_lowest_price:
                send_price_alert(
                    to_email=flight.Email,
                    subject="✈️ 機票價格下降通知",
                    content=(
                        f"{flight.From} → {flight.To}\n"
                        f"日期：{flight.Date}\n"
                        f"昨日最低價：NT${flight.go_last_lowest_price}\n"
                        f"今日最低價：NT${today_go_lowest}"
                    )
                )
                flight.go_last_lowest_price = today_go_lowest

            if flight.back_last_lowest_price is None:

                flight.back_last_lowest_price = today_back_lowest

            elif today_back_lowest < flight.back_last_lowest_price:
                send_price_alert(
                    to_email=flight.Email,
                    subject="✈️ 機票價格下降通知",
                    content=(
                        f"{flight.From} → {flight.To}\n"
                        f"日期：{flight.Date}\n"
                        f"昨日最低價：NT${flight.back_last_lowest_price}\n"
                        f"今日最低價：NT${today_back_lowest}"
                    )
                )
                flight.back_last_lowest_price = today_back_lowest

        db.session.commit()



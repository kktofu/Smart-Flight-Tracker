from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from forms import CreateFlightForm

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

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    form = CreateFlightForm()
    if form.validate_on_submit():
        data = form.To.data
        print(data)
        return render_template("header.html",form=form)
    return render_template("header.html",form=form)

if __name__ == "__main__":
    app.run(debug=True)
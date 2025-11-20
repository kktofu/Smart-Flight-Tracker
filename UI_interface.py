from flask import Flask,render_template,request
from forms import CreateFlightFrom

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "my_super_secret_key"


@app.route("/", methods=["GET", "POST"])
def home():
    form = CreateFlightFrom()
    if form.validate_on_submit():
        data = form.To.data
        print(data)
        return render_template("header.html",form=form)
    return render_template("header.html",form=form)

if __name__ == "__main__":
    app.run(debug=True)
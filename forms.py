from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired,Regexp

class CreateFlightForm(FlaskForm):
    From = StringField("出發地(IATA Code)", validators=[DataRequired(),Regexp(r'^[A-Z]{3}$',message="IATA Code 必須是三個大寫英文，例如 TPE")])
    To = StringField("目的地(IATA Code)", validators=[DataRequired(),Regexp(r'^[A-Z]{3}$',message="IATA Code 必須是三個大寫英文，例如 NRT")])
    Date = StringField("旅行日期", validators=[DataRequired(),
        Regexp(r'^\d{4}/\d{2}/\d{2} - \d{4}/\d{2}/\d{2}$',
        message="日期格式必須是：YYYY/MM/DD - YYYY/MM/DD")])
    Class_name = SelectField("選擇艙等", validators=[DataRequired()],choices=[('2,經濟艙','經濟艙'),('3,豪華經濟艙','豪華經濟艙')])
    Submit = SubmitField("查詢票價")
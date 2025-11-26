from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired,Regexp,Email
import email_validator

class CreateFlightForm(FlaskForm):
    From = StringField("出發地(IATA Code)", validators=[DataRequired(),Regexp(r'^[A-Z]{3}$',message="IATA Code 必須是三個大寫英文，例如 TPE")])
    To = StringField("目的地(IATA Code)", validators=[DataRequired(),Regexp(r'^[A-Z]{3}$',message="IATA Code 必須是三個大寫英文，例如 NRT")])
    Date = StringField("旅行日期", validators=[DataRequired(),
        Regexp(r'^\d{4}/\d{2}/\d{2} - \d{4}/\d{2}/\d{2}$',
        message="日期格式必須是：YYYY/MM/DD - YYYY/MM/DD")])
    Class_name = SelectField("選擇艙等", validators=[DataRequired()],choices=[('eco,經濟艙','經濟艙'),('ecoPremium,豪華經濟艙','豪華經濟艙')])
    Email = StringField("Email", validators=[DataRequired(), Email(message="請輸入正確的電子郵件")])
    Submit = SubmitField("查詢票價")
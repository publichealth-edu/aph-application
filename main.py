
from flask import Flask, render_template
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS, UploadSet
import smtplib
import os

FROM_EMAIL = os.environ.get("FROM_EMAIL")
PASSWORD = os.environ.get("PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")


class MyForm(FlaskForm):
    fname = StringField(label='What is your first name?', validators=[DataRequired()])
    mname = StringField(label='What is your middle name? (Skip if not applicable)')
    lname = StringField(label='What is your last name?', validators=[DataRequired()])
    email = StringField(label='What is your email address?', validators=[Email(), DataRequired(), Length(min=6)])
    cemail = StringField(label='Please confirm your email address', validators=[Email(), DataRequired(), Length(min=6)])
    phone = StringField(label="What is your phone number (Please add your country\n's dialing code)", validators=[DataRequired()])
    cphone = StringField(label="Please confirm your phone number", validators=[DataRequired()])
    citizen = StringField(label='What is your country of birth?', validators=[DataRequired()])
    residence = StringField(label='What is your country of residence?', validators=[DataRequired()])
    category = SelectField('What membership category are you applying for?', choices=["", "Graduate Member", "Associate Member", "Member", "Fellow", "Institution Member"], validators=[DataRequired()])
    support = FileField(label='Please upload supporting statement here', validators=[DataRequired()])
    resume = FileField(label='Please upload your resume here', validators=[DataRequired()])
    cert = FileField(label='Please upload your certificate here', validators=[DataRequired()])
    reference = FileField(label='Please upload your resume here', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'hello_world'
app.config['UPLOADED_ATTACHMENTS_DEST'] = 'uploads'

files = UploadSet('attachments', DOCUMENTS)
configure_uploads(app, files)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = MyForm()
    if form.validate_on_submit():
        fname = form.fname.data
        mname = form.mname.data
        lname = form.lname.data
        email = form.email.data
        phone = form.phone.data
        citizen = form.citizen.data
        residence = form.residence.data
        category = form.category.data
        support = form.support.data
        resume = form.resume.data
        cert = form.cert.data
        reference = form.reference.data

        filename = files.save(support)
        filename = files.save(resume)
        filename = files.save(cert)
        filename = files.save(reference)

        with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
            connection.starttls()
            connection.login(user=FROM_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=FROM_EMAIL,
                to_addrs=TO_EMAIL,
                msg=f"Subject: New APH Membership Application\n\nFirst name: {fname}\n\nMiddle name: {mname}\n\nLast name: {lname}\n\nEmail: {email}\n\nPhone: {phone}\n\nCountry of Citizenship: {citizen}\n\nCountry of Residence: {residence}\n\nCategory being applied for: {category}"
                    )
        
        
        return render_template('success.html')
    return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)


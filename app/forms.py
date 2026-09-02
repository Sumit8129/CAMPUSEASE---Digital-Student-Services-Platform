from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    roll_number = StringField('Roll Number', validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_roll_number(self, roll_number):
        user = User.query.filter_by(roll_number=roll_number.data).first()
        if user:
            raise ValidationError('That roll number is already registered. Please log in.')

class LoginForm(FlaskForm):
    roll_number = StringField('Roll Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class NoticeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post Notice')

class StudyMaterialForm(FlaskForm):
    title = StringField('Resource Title', validators=[DataRequired(), Length(min=3, max=200)])
    subject = StringField('Subject Name', validators=[DataRequired(), Length(min=2, max=100)])
    semester = SelectField('Semester', choices=[
        ('Semester 1', 'Semester 1'), ('Semester 2', 'Semester 2'), 
        ('Semester 3', 'Semester 3'), ('Semester 4', 'Semester 4'), 
        ('Semester 5', 'Semester 5'), ('Semester 6', 'Semester 6'), 
        ('Semester 7', 'Semester 7'), ('Semester 8', 'Semester 8')
    ], validators=[DataRequired()])
    file_url = StringField('File Link (Google Drive, Dropbox, OneDrive, etc.)', validators=[DataRequired()])
    submit = SubmitField('Upload Material')

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(min=3, max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    event_date = StringField('Event Date & Time', validators=[DataRequired()], render_kw={"placeholder": "e.g., October 15, 2026 - 10:00 AM"})
    location = StringField('Location / Mode', validators=[DataRequired()], render_kw={"placeholder": "e.g., Main Auditorium / Online"})
    submit = SubmitField('Create Event')

# NEW: Form for posting career opportunities
class OpportunityForm(FlaskForm):
    title = StringField('Role / Position Title', validators=[DataRequired(), Length(min=3, max=200)], render_kw={"placeholder": "e.g., Software Engineering Intern"})
    company = StringField('Company / Organization Name', validators=[DataRequired(), Length(min=2, max=100)], render_kw={"placeholder": "e.g., Google"})
    opp_type = SelectField('Opportunity Type', choices=[
        ('Internship', 'Internship'), 
        ('Job', 'Full-Time Job'), 
        ('Hackathon', 'Hackathon'), 
        ('Competition', 'Competition')
    ], validators=[DataRequired()])
    stipend = StringField('Stipend / Salary / Prize (Optional)', validators=[Length(max=50)], render_kw={"placeholder": "e.g., ₹30,000 / month"})
    description = TextAreaField('Role Description & Requirements', validators=[DataRequired()])
    apply_url = StringField('Application Link / URL', validators=[DataRequired()], render_kw={"placeholder": "https://company.com/careers/apply"})
    submit = SubmitField('Post Opportunity')
    from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    roll_number = StringField('Roll Number', validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_roll_number(self, roll_number):
        user = User.query.filter_by(roll_number=roll_number.data).first()
        if user:
            raise ValidationError('That roll number is already registered. Please log in.')

class LoginForm(FlaskForm):
    roll_number = StringField('Roll Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class NoticeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post Notice')

class StudyMaterialForm(FlaskForm):
    title = StringField('Resource Title', validators=[DataRequired(), Length(min=3, max=200)])
    subject = StringField('Subject Name', validators=[DataRequired(), Length(min=2, max=100)])
    semester = SelectField('Semester', choices=[
        ('Semester 1', 'Semester 1'), ('Semester 2', 'Semester 2'), 
        ('Semester 3', 'Semester 3'), ('Semester 4', 'Semester 4'), 
        ('Semester 5', 'Semester 5'), ('Semester 6', 'Semester 6'), 
        ('Semester 7', 'Semester 7'), ('Semester 8', 'Semester 8')
    ], validators=[DataRequired()])
    file_url = StringField('File Link (Google Drive, Dropbox, OneDrive, etc.)', validators=[DataRequired()])
    submit = SubmitField('Upload Material')

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(min=3, max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    event_date = StringField('Event Date & Time', validators=[DataRequired()], render_kw={"placeholder": "e.g., October 15, 2026 - 10:00 AM"})
    location = StringField('Location / Mode', validators=[DataRequired()], render_kw={"placeholder": "e.g., Main Auditorium / Online"})
    submit = SubmitField('Create Event')

class OpportunityForm(FlaskForm):
    title = StringField('Role / Position Title', validators=[DataRequired(), Length(min=3, max=200)], render_kw={"placeholder": "e.g., Software Engineering Intern"})
    company = StringField('Company / Organization Name', validators=[DataRequired(), Length(min=2, max=100)], render_kw={"placeholder": "e.g., Google"})
    opp_type = SelectField('Opportunity Type', choices=[
        ('Internship', 'Internship'), 
        ('Job', 'Full-Time Job'), 
        ('Hackathon', 'Hackathon'), 
        ('Competition', 'Competition')
    ], validators=[DataRequired()])
    stipend = StringField('Stipend / Salary / Prize (Optional)', validators=[Length(max=50)], render_kw={"placeholder": "e.g., ₹30,000 / month"})
    description = TextAreaField('Role Description & Requirements', validators=[DataRequired()])
    apply_url = StringField('Application Link / URL', validators=[DataRequired()], render_kw={"placeholder": "https://company.com/careers/apply"})
    submit = SubmitField('Post Opportunity')

# NEW: Form for updating passwords
class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')
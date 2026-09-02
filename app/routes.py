import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Notice, StudyMaterial, Event, Opportunity
from app.forms import LoginForm, RegistrationForm, NoticeForm, StudyMaterialForm, EventForm, OpportunityForm, UpdatePasswordForm

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(full_name=form.full_name.data, roll_number=form.roll_number.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('register.html', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(roll_number=form.roll_number.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            
            # --- SECURE ROLL NUMBER ADMIN CHECK ---
            admin_roll = os.environ.get('ADMIN_ROLL_NUMBER')
            if admin_roll and str(user.roll_number) == str(admin_roll):
                if user.role != 'admin':
                    user.role = 'admin'
                    db.session.commit()
            # --------------------------------------
            
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check roll number and password.', 'danger')
            
    return render_template('login.html', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.old_password.data):
            current_user.password_hash = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated successfully!', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('Current password is incorrect. Please try again.', 'danger')
            
    return render_template('profile.html', form=form)

# --- NOTICES ROUTES (with Global Search Support) ---
@main.route("/notices")
@login_required
def notices():
    search_query = request.args.get('q', '', type=str)
    if search_query:
        all_notices = Notice.query.filter(
            (Notice.title.ilike(f'%{search_query}%')) | 
            (Notice.content.ilike(f'%{search_query}%'))
        ).order_by(Notice.date_posted.desc()).all()
    else:
        all_notices = Notice.query.order_by(Notice.date_posted.desc()).all()
    return render_template("notices.html", notices=all_notices, search_query=search_query)

@main.route("/notice/new", methods=['GET', 'POST'])
@login_required
def new_notice():
    if current_user.role != 'admin':
        flash('Access Denied: Only administrators can post notices.', 'danger')
        return redirect(url_for('main.notices'))
        
    form = NoticeForm()
    if form.validate_on_submit():
        notice = Notice(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(notice)
        db.session.commit()
        flash('Notice has been successfully posted!', 'success')
        return redirect(url_for('main.notices'))
        
    return render_template('create_notice.html', form=form)

@main.route("/notice/delete/<int:notice_id>", methods=['POST'])
@login_required
def delete_notice(notice_id):
    if current_user.role != 'admin':
        flash('Access Denied.', 'danger')
        return redirect(url_for('main.notices'))
    notice = Notice.query.get_or_404(notice_id)
    db.session.delete(notice)
    db.session.commit()
    flash('Notice deleted successfully.', 'success')
    return redirect(url_for('main.notices'))

# --- STUDY MATERIALS ROUTES ---
@main.route("/materials")
@login_required
def materials():
    semester_filter = request.args.get('semester', '', type=str)
    subject_query = request.args.get('subject', '', type=str)
    
    query = StudyMaterial.query
    if semester_filter:
        query = query.filter_by(semester=semester_filter)
    if subject_query:
        query = query.filter(StudyMaterial.subject.ilike(f'%{subject_query}%'))
        
    all_materials = query.order_by(StudyMaterial.date_posted.desc()).all()
    return render_template("materials.html", materials=all_materials, semester_filter=semester_filter, subject_query=subject_query)

@main.route("/material/new", methods=['GET', 'POST'])
@login_required
def new_material():
    if current_user.role != 'admin':
        flash('Access Denied: Only administrators can upload materials.', 'danger')
        return redirect(url_for('main.materials'))
        
    form = StudyMaterialForm()
    if form.validate_on_submit():
        material = StudyMaterial(
            title=form.title.data, 
            subject=form.subject.data, 
            semester=form.semester.data,
            file_url=form.file_url.data,
            uploader=current_user
        )
        db.session.add(material)
        db.session.commit()
        flash('Study material has been successfully uploaded!', 'success')
        return redirect(url_for('main.materials'))
        
    return render_template('create_material.html', form=form)

@main.route("/material/delete/<int:material_id>", methods=['POST'])
@login_required
def delete_material(material_id):
    if current_user.role != 'admin':
        flash('Access Denied.', 'danger')
        return redirect(url_for('main.materials'))
    material = StudyMaterial.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    flash('Study material deleted successfully.', 'success')
    return redirect(url_for('main.materials'))

# --- EVENTS ROUTES ---
@main.route("/events")
@login_required
def events():
    all_events = Event.query.order_by(Event.date_posted.desc()).all()
    return render_template("events.html", events=all_events)

@main.route("/event/new", methods=['GET', 'POST'])
@login_required
def new_event():
    if current_user.role != 'admin':
        flash('Access Denied: Only administrators can create events.', 'danger')
        return redirect(url_for('main.events'))
        
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            event_date=form.event_date.data,
            location=form.location.data,
            organizer=current_user
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('main.events'))
        
    return render_template('create_event.html', form=form)

@main.route("/event/delete/<int:event_id>", methods=['POST'])
@login_required
def delete_event(event_id):
    if current_user.role != 'admin':
        flash('Access Denied.', 'danger')
        return redirect(url_for('main.events'))
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully.', 'success')
    return redirect(url_for('main.events'))

# --- OPPORTUNITIES ROUTES ---
@main.route("/opportunities")
@login_required
def opportunities():
    opp_type_filter = request.args.get('type', '', type=str)
    query = Opportunity.query
    if opp_type_filter:
        query = query.filter_by(opp_type=opp_type_filter)
        
    all_opps = query.order_by(Opportunity.date_posted.desc()).all()
    return render_template("opportunities.html", opportunities=all_opps, opp_type_filter=opp_type_filter)

@main.route("/opportunity/new", methods=['GET', 'POST'])
@login_required
def new_opportunity():
    if current_user.role != 'admin':
        flash('Access Denied: Only administrators can post opportunities.', 'danger')
        return redirect(url_for('main.opportunities'))
        
    form = OpportunityForm()
    if form.validate_on_submit():
        opp = Opportunity(
            title=form.title.data,
            company=form.company.data,
            opp_type=form.opp_type.data,
            stipend=form.stipend.data,
            description=form.description.data,
            apply_url=form.apply_url.data,
            poster=current_user
        )
        db.session.add(opp)
        db.session.commit()
        flash('Opportunity posted successfully!', 'success')
        return redirect(url_for('main.opportunities'))
        
    return render_template('create_opportunity.html', form=form)

@main.route("/opportunity/delete/<int:opp_id>", methods=['POST'])
@login_required
def delete_opportunity(opp_id):
    if current_user.role != 'admin':
        flash('Access Denied.', 'danger')
        return redirect(url_for('main.opportunities'))
    opp = Opportunity.query.get_or_404(opp_id)
    db.session.delete(opp)
    db.session.commit()
    flash('Opportunity deleted successfully.', 'success')
    return redirect(url_for('main.opportunities'))

@main.route("/health")
def health():
    return {"status": "ok", "application": "CampusEase"}
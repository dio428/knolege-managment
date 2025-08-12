import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from .forms import LoginForm, UserCreationForm, ProductForm, TipSubmissionForm
from .models import User, Product, Tip, Attachment
from . import db
from .utils import admin_required

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.dashboard'))
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    tips = current_user.tips.all()
    approved_tips_count = current_user.tips.filter_by(is_approved=True).count()
    stars_earned = db.session.query(db.func.sum(Tip.rating)).filter(Tip.user_id == current_user.id, Tip.is_approved == True).scalar() or 0

    return render_template('dashboard.html', title='Dashboard', tips=tips, approved_tips_count=approved_tips_count, stars_earned=stars_earned)

@bp.route('/admin/users', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_users():
    form = UserCreationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, is_admin=form.is_admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully.')
        return redirect(url_for('main.manage_users'))
    users = User.query.all()
    return render_template('admin/manage_users.html', title='Manage Users', form=form, users=users)

@bp.route('/admin/products', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_products():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data)
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully.')
        return redirect(url_for('main.manage_products'))
    products = Product.query.all()
    return render_template('admin/manage_products.html', title='Manage Products', form=form, products=products)

@bp.route('/submit_tip', methods=['GET', 'POST'])
@login_required
def submit_tip():
    form = TipSubmissionForm()
    form.product.choices = [(p.id, p.name) for p in Product.query.order_by('name')]

    if form.validate_on_submit():
        tip = Tip(
            title=form.title.data,
            content=form.content.data,
            product_id=form.product.data,
            user_id=current_user.id
        )
        db.session.add(tip)
        db.session.commit() # Commit to get tip.id for attachments

        files = request.files.getlist(form.attachments.name)
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                upload_path = os.path.join('app', 'static', 'uploads', filename)
                file.save(upload_path)
                attachment = Attachment(filename=filename, tip_id=tip.id)
                db.session.add(attachment)

        db.session.commit()
        flash('Your tip has been submitted for approval.')
        return redirect(url_for('main.dashboard'))

    return render_template('submit_tip.html', title='Submit Tip', form=form)

@bp.route('/admin/tips')
@login_required
@admin_required
def manage_tips():
    tips = Tip.query.all()
    return render_template('admin/manage_tips.html', title='Manage Tips', tips=tips)

@bp.route('/admin/tip/<int:tip_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_tip(tip_id):
    tip = Tip.query.get_or_404(tip_id)
    tip.is_approved = True
    db.session.commit()
    flash('Tip approved successfully.')
    return redirect(url_for('main.manage_tips'))

@bp.route('/admin/tip/<int:tip_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_tip(tip_id):
    tip = Tip.query.get_or_404(tip_id)
    db.session.delete(tip)
    db.session.commit()
    flash('Tip rejected successfully.')
    return redirect(url_for('main.manage_tips'))

@bp.route('/admin/tip/<int:tip_id>/rate', methods=['POST'])
@login_required
@admin_required
def rate_tip(tip_id):
    tip = Tip.query.get_or_404(tip_id)
    rating = request.form.get('rating')
    if rating:
        tip.rating = int(rating)
        db.session.commit()
        flash('Tip rated successfully.')
    return redirect(url_for('main.manage_tips'))

@bp.route('/admin/reports')
@login_required
@admin_required
def reports():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    query = db.session.query(
        User.username,
        db.func.sum(Tip.rating).label('total_stars')
    ).join(Tip, User.id == Tip.user_id).filter(Tip.is_approved == True)

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        query = query.filter(Tip.created_at >= start_date)
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        query = query.filter(Tip.created_at <= end_date)

    users_report = query.group_by(User.username).order_by(db.desc('total_stars')).all()

    return render_template('admin/reports.html', title='Reports', users_report=users_report, start_date=start_date_str, end_date=end_date_str)

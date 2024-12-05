from flask import render_template, redirect, session, url_for, flash, request
from app import app, db
from app.forms import RegistrationForm, LoginForm, OrderForm, PortfolioForm
from app.models import User, Service, Order, PortfolioItem
from flask_login import logout_user, login_required
from flask_login import current_user
from flask_login import login_user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,)  # Хэшируйте пароль!
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):  # Используйте метод check_password
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Логика для обновления профиля
        current_user.username = request.form.get('username')
        current_user.email = request.form.get('email')
        db.session.commit()
        flash('Профиль обновлен!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.', 'success')
    return redirect(url_for('index'))

@app.route('/services')
def services():
    services_list = Service.query.all()
    return render_template('services.html', services=services_list)

@app.route('/order/<int:service_id>', methods=['GET', 'POST'])
@login_required
def order(service_id):
    form = OrderForm()
    
    # Заполнение списка услуг
    form.service_id.choices = [(s.id, s.name) for s in Service.query.all()]
    
    if form.validate_on_submit():
        new_order = Order(user_id=1, service_id=form.service_id.data)  # Замените на текущего пользователя
        db.session.add(new_order)
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('order.html', form=form)

@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    form = PortfolioForm()
    
    if form.validate_on_submit():
        new_item = PortfolioItem(user_id=1,
        image_url=form.image_url.data,
        description=form.description.data)  # Замените на текущего пользователя
        db.session.add(new_item)
        db.session.commit()
        flash('Portfolio item added!', 'success')
        return redirect(url_for('portfolio'))
    
    return render_template('portfolio.html', form=form)

# Обработка ошибок
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/set_theme/<theme>')
@login_required
def set_theme(theme):
    if theme in ['light', 'dark']:
        session['theme'] = theme
        flash('Тема изменена!', 'success')
    return redirect(url_for('profile'))
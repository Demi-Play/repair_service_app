from flask import render_template, redirect, session, url_for, flash, request
from app import app, db
from app.forms import RegistrationForm, LoginForm, OrderForm, PortfolioForm
from app.models import Payment, User, Service, Order, PortfolioItem
from flask_login import logout_user, login_required
from flask_login import current_user
from flask_login import login_user

@app.route('/')
def index():
    portfolio_items = PortfolioItem.query.all()
    return render_template('index.html', portfolio_items=portfolio_items)

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
        elif user and user.password_hash == form.password.data:
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

@app.route('/add_to_cart/<int:service_id>')
@login_required
def add_to_cart(service_id):
    service = Service.query.get_or_404(service_id)
    
    # Создаем новый заказ
    new_order = Order(user_id=current_user.id, service_id=service.id, status='pending')
    db.session.add(new_order)
    db.session.commit()
    
    flash(f'Услуга "{service.name}" добавлена в корзину!', 'success')
    return redirect(url_for('services'))  # Перенаправление на страницу с услугами

@app.route('/cart')
@login_required
def cart():
    # Получаем все заказы текущего пользователя
    orders = Order.query.filter_by(user_id=current_user.id).all()
    total_price = sum(order.service.price for order in orders)

    return render_template('cart.html', orders=orders, total_price=total_price)

@app.route('/checkout')
@login_required
def checkout():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    
    if not orders:
        flash('Ваша корзина пуста!', 'warning')
        return redirect(url_for('services'))

    # Имитация оплаты
    for order in orders:
        payment = Payment(order_id=order.id, amount=order.service.price, payment_status='completed')
        db.session.add(payment)

        # Удаляем заказ после успешной оплаты
        db.session.delete(order)

    db.session.commit()
    
    flash('Оплата прошла успешно!', 'success')
    
    return redirect(url_for('index'))  # Перенаправление на главную страницу

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
        new_item = PortfolioItem(
            user_id=current_user.id,  # Замените на текущего пользователя
            image_url=form.image_url.data,
            description=form.description.data
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Элемент портфолио добавлен!', 'success')
        return redirect(url_for('portfolio'))
    
    # Извлечение всех элементов портфолио из базы данных
    portfolio_items = PortfolioItem.query.all()
    
    return render_template('portfolio.html', form=form, portfolio_items=portfolio_items)

# Обработка ошибок
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# @app.route('/set_theme/<theme>', methods=['POST'])
# @login_required
# def set_theme(theme):
#     if theme in ['light', 'dark']:
#         session['theme'] = theme
#         flash('Тема изменена!', 'success')
#     return redirect(url_for('profile'))

@app.route('/moderate')
@login_required
def moderate():
    if current_user.role != 'moderator':
        flash('У вас нет прав доступа к этой странице.', 'danger')
        return redirect(url_for('index'))
    
    # Логика для модерации
    return render_template('moderate.html')

@app.route('/moderate/services', methods=['GET', 'POST'])
@login_required
def manage_services():
    if current_user.role != 'moderator':
        flash('У вас нет прав доступа к этой странице.', 'danger')
        return redirect(url_for('index'))

    services = Service.query.all()
    
    if request.method == 'POST':
        # Добавление новой услуги
        new_service = Service(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price']
        )
        db.session.add(new_service)
        db.session.commit()
        flash('Услуга добавлена!', 'success')
        return redirect(url_for('manage_services'))

    return render_template('manage_services.html', services=services)

@app.route('/moderate/orders', methods=['GET'])
@login_required
def manage_orders():
    if current_user.role != 'moderator':
        flash('У вас нет прав доступа к этой странице.', 'danger')
        return redirect(url_for('index'))

    orders = Order.query.all()
    return render_template('manage_orders.html', orders=orders)

@app.route('/moderate/portfolio', methods=['GET', 'POST'])
@login_required
def manage_portfolio():
    if current_user.role != 'moderator':
        flash('У вас нет прав доступа к этой странице.', 'danger')
        return redirect(url_for('index'))

    portfolio_items = PortfolioItem.query.all()

    if request.method == 'POST':
        # Добавление нового элемента портфолио
        new_item = PortfolioItem(
            user_id=current_user.id,  # Или другой ID пользователя, если нужно
            image_url=request.form['image_url'],
            description=request.form['description']
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Элемент портфолио добавлен!', 'success')
        return redirect(url_for('manage_portfolio'))

    return render_template('manage_portfolio.html', portfolio_items=portfolio_items)
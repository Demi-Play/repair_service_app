from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.config import Config

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'IjQyMzQxZTJkMzA0ZGY2OWI1MjJlOGY4NWJlZTA5YjlkYWQyNzkyOGMi.Z1HLUw.MFNmS9xSMzk2FRbmeZvb39z-0MU'
app.config['SESSION_TYPE'] = 'filesystem'

csrf = CSRFProtect(app)
csrf.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

admin = Admin(app, name='Административная панель', template_mode='bootstrap3')

# Импорт моделей

from app.models import User, Service, Order, PortfolioItem, Payment

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Service, db.session))
admin.add_view(AdminModelView(Order, db.session))
admin.add_view(AdminModelView(PortfolioItem, db.session))
admin.add_view(AdminModelView(Payment, db.session))

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def before_request():
    if 'theme' not in session:
        session['theme'] = 'light'  # Установите тему по умолчанию

# Импорт маршрутов после инициализации приложения
from app import views



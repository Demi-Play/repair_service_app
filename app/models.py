import app
from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='client')  # admin, moderator, client
    orders = db.relationship('Order', backref='user', lazy=True)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    orders = db.relationship('Order', backref='service', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    status = db.Column(db.String(20))  # pending, completed, cancelled
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    amount = db.Column(db.Float)
    payment_status = db.Column(db.String(20))  # pending, completed, failed
    payment_date = db.Column(db.DateTime)

class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    

# with app.app.app_context():
    # services = [
    #         Service(name="Косметический ремонт", description="Обновление интерьера с минимальными затратами.", price=1500),
    #         Service(name="Капитальный ремонт", description="Полный ремонт квартиры с заменой всех коммуникаций.", price=3000),
    #         Service(name="Установка окон и дверей", description="Установка пластиковых окон и межкомнатных дверей.", price=5000),
    #         Service(name="Электромонтажные работы", description="Проведение электропроводки.", price=2000),
    #         Service(name="Сантехнические работы", description="Установка и замена сантехники.", price=2500),
    #         Service(name="Отделка балконов", description="Утепление и отделка балконов под ключ.", price=40000),
    #         Service(name="Дизайн интерьера", description="Разработка индивидуального дизайна интерьера.", price=10000),
    #     ]

    #     # Добавление услуг в базу данных
    # db.session.bulk_save_objects(services)
# # Создание портфолио
#   user_id = 4
#   portfolio_items = [
#         PortfolioItem(user_id=user_id, image_url='url_to_image_1.jpg', description='Косметический ремонт в квартире'),
#         PortfolioItem(user_id=user_id, image_url='url_to_image_2.jpg', description='Капитальный ремонт ванной комнаты'),
#         PortfolioItem(user_id=user_id, image_url='url_to_image_3.jpg', description='Установка окон в загородном доме'),
#         PortfolioItem(user_id=user_id, image_url='url_to_image_4.jpg', description='Электромонтажные работы в офисе'),
#         PortfolioItem(user_id=user_id, image_url='url_to_image_5.jpg', description='Сантехнические работы в квартире'),
#         PortfolioItem(user_id=user_id, image_url='url_to_image_6.jpg', description='Отделка балкона под ключ'),
#         PortfolioItem(user_id=user_id, image_url='url_to_image_7.jpg', description='Дизайн интерьера спальни'),
#         PortfolioItem(user_id=user_id, image_url='url_to_image_8.jpg', description='Ремонт кухни с нуля'),
#         PortfolioItem(user_id=user_id, image_url='url_to_image_9.jpg', description='Обновление интерьера детской комнаты'),
#         PortfolioItem(user_id=user_id, image_url='url_to_image_10.jpg', description='Капитальный ремонт коммерческого помещения'),
#         PortfolioItem(user_id=user_id, image_url='url_to_image_11.jpg', description='Установка межкомнатных дверей'),
#         PortfolioItem(user_id=user_id, image_url='url_to_image_12.jpg', description='Ремонт санузла в новостройке'),
#         PortfolioItem(user_id=user_id, image_url='url_to_image_13.jpg', description='Декорирование стен с помощью обоев'),
#     ]

#     # Добавление портфолио в базу данных
#   db.session.bulk_save_objects(portfolio_items)
#   db.session.commit()
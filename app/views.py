from app import app

@app.route('/')
def index():
    return "Welcome to the Repair Service App"

@app.route('/services')
def services():
    return "Логика для отображения доступных услуг"

@app.route('/order/<int:service_id>', methods=['POST'])
def order(service_id):
    return "Логика для оформления заказа на услугу"
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, message_queue=app.config['REDIS_URL'])
    limiter.init_app(app)
    
    from app.routes import main, auth, tickets, messages
    from app.admin.routes import admin
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(tickets)
    app.register_blueprint(messages)
    app.register_blueprint(admin, url_prefix='/admin')
    
    with app.app_context():
        db.create_all()
    
    return app

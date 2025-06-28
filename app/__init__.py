from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    csrf = CSRFProtect(app)
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    from app import models  # Import models to register them with SQLAlchemy
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))  
    load_user.__name__ = 'load_user'
    
    
    from app.routes import register_blueprints
    register_blueprints(app)
    
    # from app.routes import admin
    # app.register_blueprint(admin.bp)
    
    return app
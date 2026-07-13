from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended  import JWTManager
from flask_cors import CORS
from flask_caching import Cache 
from redis import Redis 
from celery import Celery

from backend.config import LocalDevelopmentConfig



db =SQLAlchemy()
jwt=JWTManager()
cache=Cache()
redis=Redis()
celery=Celery()

def create_app():
    app=Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    CORS(app, origins=["http://localhost:5173"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"], allow_headers=["Content-Type", "Authorization"])
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    from backend.controllers.authcontrollers import auth_bp
    from backend.controllers.admin_controller import admin_bp
    from backend.controllers.trek_controller import trek_bp
    from backend.controllers.user_controller import user_bp
 
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(trek_bp)
    app.register_blueprint(user_bp)
   
    return app

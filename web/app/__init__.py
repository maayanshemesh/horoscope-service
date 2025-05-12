"""
Flask Application Factory Module

This module implements the application factory pattern for Flask, creating and configuring
the application instance with necessary extensions and blueprints.

The create_app() function serves as the application factory, allowing for flexible
instantiation of the Flask application in different contexts (development, testing, production).
This pattern facilitates easier testing and configuration management by deferring
the creation of the application until runtime.

Key components:
- Flask application initialization and configuration
- Redis connection establishment using configuration parameters
- Blueprint registration for routing and view separation
"""

from flask import Flask
import redis
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config['REDIS'] = redis.Redis(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        decode_responses=True
    )

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app

"""
Application Entry Point Module

This module serves as the primary entry point for the Flask application,
creating the application instance and providing configuration for both
development and production environments.

Key functions:
- Creates the application instance by calling the application factory
- Provides development server configuration when run directly
- Serves as the WSGI entry point for production servers like Gunicorn

The 'app' object created here is referenced directly in the Dockerfile's
CMD instruction: 'gunicorn --bind 0.0.0.0:5000 run:app'
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
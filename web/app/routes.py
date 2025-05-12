"""
Application Routes Module

This module defines the application's URL routes and request handlers,
implementing both web UI and API endpoints for horoscope data.

Endpoints:
- / : Application home page
- /horoscope : Web UI for displaying horoscope data
- /api/horoscope/<sign> : RESTful API endpoint for retrieving horoscope data in JSON format

Features:
- Input validation against a predefined list of valid zodiac signs
- Consistent error handling for invalid inputs and failed operations
- Separation between UI rendering and API responses
- Flash messaging for user feedback in the web interface

The Blueprint architecture allows for modular route organization and potential
future expansion with additional feature sets.
"""

from flask import Blueprint, render_template, request, jsonify, current_app, flash
from app.horoscope import get_horoscope_for_sign

main_bp = Blueprint('main', __name__)

VALID_SIGNS = [
    'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
    'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
]

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/horoscope')
def horoscope_page():
    sign = request.args.get('sign', '').lower()

    if sign not in VALID_SIGNS:
        flash("Please select a valid zodiac sign.", "error")
        return render_template('index.html')

    horoscope_data = get_horoscope_for_sign(sign, current_app.config['REDIS'])
    return render_template('horoscope.html', sign=sign.capitalize(), horoscope=horoscope_data)

@main_bp.route('/api/horoscope/<sign>')
def horoscope_api(sign):
    sign = sign.lower()

    if sign not in VALID_SIGNS:
        return jsonify({'error': 'Invalid zodiac sign'}), 400

    horoscope_data = get_horoscope_for_sign(sign, current_app.config['REDIS'])

    if "error" in horoscope_data:
        return jsonify({'error': horoscope_data["error"]}), 500

    return jsonify({'sign': sign, 'horoscope': horoscope_data})

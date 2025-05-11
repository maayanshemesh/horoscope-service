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
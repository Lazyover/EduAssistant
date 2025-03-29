from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.services.recommend_service import RecommendService

recommend_bp = Blueprint('recommend', __name__, url_prefix='/recommend')

# @recommend_bp.route('/test')
# def test():
#     return RecommendService.test()

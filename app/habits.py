from flask import Blueprint, request, jsonify
from app import db
from app.models import Habit
from flask_jwt_extended import jwt_required, get_jwt_identity

habits_bp = Blueprint("habits", __name__)

@habits_bp.route("/", methods=["GET"])
@jwt_required()
def get_habits():
    user_id = get_jwt_identity()
    habits = Habit.query.filter_by(user_id=user_id).all()
    return jsonify([h.to_dict() for h in habits])

@habits_bp.route("/", methods=["POST"])
@jwt_required()
def create_habit():
    user_id = get_jwt_identity()
    data = request.get_json()
    habit = Habit(name=data["name"], user_id=user_id)
    db.session.add(habit)
    db.session.commit()
    return jsonify(habit.to_dict()), 201

@habits_bp.route("/<int:habit_id>/done", methods=["PUT"])
@jwt_required()
def mark_done(habit_id):
    user_id = get_jwt_identity()
    habit = Habit.query.filter_by(id=habit_id, user_id=user_id).first_or_404()
    msg = habit.mark_done()
    db.session.commit()
    return jsonify({"message": msg, "habit": habit.to_dict()})

@habits_bp.route("/<int:habit_id>", methods=["DELETE"])
@jwt_required()
def delete_habit(habit_id):
    user_id = get_jwt_identity()
    habit = Habit.query.filter_by(id=habit_id, user_id=user_id).first_or_404()
    db.session.delete(habit)
    db.session.commit()
    return jsonify({"message": "Deleted"})
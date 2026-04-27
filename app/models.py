from app import db
from datetime import datetime, date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    habits = db.relationship("Habit", backref="user", lazy=True)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    streak = db.Column(db.Integer, default=0)
    last_completed = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def mark_done(self):
        today = date.today()
        if self.last_completed == today:
            return "already done today"
        from datetime import timedelta
        if self.last_completed == today - timedelta(days=1):
            self.streak += 1
        else:
            self.streak = 1
        self.last_completed = today
        return "done"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "streak": self.streak,
            "last_completed": str(self.last_completed),
        }
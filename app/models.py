from app import db

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(50), nullable=False)
    game_number = db.Column(db.Integer, nullable=False)
    game_round = db.Column(db.Integer, nullable=False)
    point = db.Column(db.Integer, nullable=False, default=0)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    submitted = db.Column(db.Boolean, nullable=False, default=False)

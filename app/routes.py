from flask import Blueprint, jsonify, flash, render_template, redirect, request, url_for, session
from app.models import Score
from app.forms import ScoreForm
from app import db
from collections import defaultdict
import datetime as dt

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    if 'google_token' in session:
        return render_template('logged_in_home.html')
    else:
        return render_template('home.html')

@bp.route('/input-score', methods=['GET', 'POST'])
def input_score():
    if not 'google_token' in session:
        return redirect(url_for('auth.login'))
    google_token = session.get('google_token')
    google_id = google_token['id']

    max_game_number = db.session.query(db.func.max(Score.game_number)).scalar()
    if max_game_number is None:
        max_game_number = 0

    game_number_requested = request.args.get('game', type=int)
    if game_number_requested is None:
        game_number = max_game_number + 1
    else:
        game_number = min(game_number_requested, max_game_number + 1)

    game_round = request.args.get('round', 1, type=int)

    score = Score.query.filter_by(google_id=google_id, game_number=game_number).first()
    if score is None:
        score = Score(google_id=google_id, game_number=game_number, game_round=game_round)
        db.session.add(score)
        db.session.commit()

    scores = Score.query.filter_by(google_id=google_id, game_number=game_number).order_by(Score.game_round).all()
    form = ScoreForm()
    return render_template('input_score.html', form=form, score=score, game_number=game_number, game_round=game_round, scores=scores)


@bp.route('/submit-score', methods=['POST'])
def submit_score():
    if not 'google_token' in session:
        return redirect(url_for('auth.login'))

    google_token = session.get('google_token')
    google_id = google_token['id']

    data = request.get_json()
    scores = data.get('scores')
    game_number = data.get('game_number')

    if len(scores) != 10:
        return jsonify({'error': 'Invalid scores length'}), 400
    if any(score < 0 or score > 10 for score in scores):
        return jsonify({'error': 'Invalid score value'}), 400

    for game_round, score_point in enumerate(scores, start=1):
        score = Score.query.filter_by(google_id=google_id, game_number=game_number, game_round=game_round).first()

        if score is not None:
            score.point = score_point
            score.submitted = True
        else:
            score = Score(google_id=google_id, game_number=game_number, game_round=game_round, point=score_point, submitted=True)
            db.session.add(score)

        print(f"score: game_number={game_number}, game_round={game_round}, point={score.point}")

    db.session.commit()

    flash('Scores submitted')
    return jsonify({'message': 'Scores submitted successfully'}), 200


@bp.route('/view-scores', methods=['GET'])
def view_scores():
    if not 'google_token' in session:
        return redirect(url_for('auth.login'))
    google_token = session.get('google_token')
    google_id = google_token['id']

    scores = Score.query.filter_by(google_id=google_id).order_by(Score.game_number, Score.game_round).all()

    scores_dict = defaultdict(dict)

    grouped_scores = {}
    for score in scores:
        scores_dict[score.game_number][score.game_round] = score.point
        if score.game_number not in grouped_scores:
            grouped_scores[score.game_number] = []
        grouped_scores[score.game_number].append(score)

    for game_number, score in grouped_scores.items():
        if len(score) < 10 or not all(s.submitted for s in score):
            del scores_dict[game_number]

    totals = {game_number: sum(game_scores.values()) for game_number, game_scores in scores_dict.items()}
    timestamps = {score.game_number: score.timestamp.strftime("%Y/%m/%d %H:%M:%S") for score in scores}

    return render_template('view_scores.html', scores=scores_dict, totals=totals, timestamps=timestamps)

@bp.route('/rank', methods=['GET'])
def rank():
    if not 'google_token' in session:
        return redirect(url_for('auth.login'))
    google_token = session.get('google_token')
    google_id = google_token['id']

    return render_template('rank.html')






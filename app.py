
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Competitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    state = db.Column(db.String(150), nullable=False)

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    state = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(150), nullable=True)
    
class Result(db.Model):
    competition_id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Float)

@app.route('/')
def index():
    competitors = Competitor.query.order_by(Competitor.id.asc()).all()
    competitions = Competition.query.order_by(Competition.id.asc()).all()
    return render_template('index.html', competitors=competitors, competitions=competitions)

@app.route('/seed', methods=['GET', 'POST'])
def seed():
    db.session.query(Competitor).delete()
    db.session.add(Competitor(name='Luke Carrot', city='Muncie', state='Indiana'))
    db.session.add(Competitor(name='Matty Hiroto Inaba', city='Honolulu', state='Hawaii'))
    db.session.add(Competitor(name='Feliks Zemdegs', city='Stratford', state='Connecticut'))

    db.session.query(Competition).delete()
    db.session.add(Competition(name='Best in West Lafayette', city='West Lafayette', state='Indiana', date='November 11, 2025'))
    db.session.add(Competition(name='Rubik\'s World Championship 2025', city='Seattle', state='Washington', date='July 4, 2025'))
    db.session.add(Competition(name='Locked in Clocked In', city='Ithaca', state='New York', date='January 7, 1999'))
    db.session.add(Competition(name='NA Championship 2026', city='Houston', state='Texas', date='August 10, 2026'))

    db.session.query(Result).delete()
    db.session.add(Result(competition_id=1, competitor_id=1, time=5.59))
    db.session.add(Result(competition_id=2, competitor_id=1, time=4.88))
    db.session.add(Result(competition_id=3, competitor_id=3, time=5.66))
    db.session.add(Result(competition_id=1, competitor_id=2, time=5.55))
    db.session.add(Result(competition_id=2, competitor_id=2, time=4.72))
    db.session.add(Result(competition_id=1, competitor_id=3, time=6.54))
    db.session.add(Result(competition_id=4, competitor_id=1, time=5.41))
    db.session.add(Result(competition_id=4, competitor_id=2, time=4.34))

    db.session.commit()

    return jsonify({}), 201

@app.route('/add_competitor', methods=['POST'])
def add_competitor():
    data = request.get_json() or {}
    competitor = Competitor(
        name=data["name"],
        city=data["city"],
        state=data["state"],
    )
    db.session.add(competitor)
    db.session.commit()
    return jsonify({
        "id": competitor.id,
        "name": competitor.name,
        "city": competitor.city,
        "state": competitor.state,
    }), 201

@app.route('/edit_competitor', methods=['PUT'])
def edit_competitor():
    data = request.get_json() or {}
    competitor_id = data["id"]
    new_name = data["name"]
    new_city = data["city"]
    new_state = data["state"]

    competitor = db.session.query(Competitor).filter(Competitor.id == competitor_id).first()
    competitor.name = new_name
    competitor.city = new_city
    competitor.state = new_state

    db.session.commit()

    return jsonify({}), 201

@app.route('/delete_competitor', methods=['DELETE'])
def delete_competitor():
    data = request.get_json() or {}
    competitor_id = data["id"]

    competitor = db.session.query(Competitor).filter(Competitor.id == competitor_id).first()
    db.session.query(Result).filter(Result.competitor_id == competitor_id).delete(synchronize_session=False)
    db.session.delete(competitor)
    db.session.commit()

    return jsonify({}), 201

@app.route('/competitor/<int:competitor_id>/results', methods=['GET'])
def competitor_results(competitor_id):
    competitor = Competitor.query.get_or_404(competitor_id)
    competitions = Competition.query.order_by(Competition.date.asc()).all()
    return render_template(
        'competitor_results.html',
        competitor=competitor,
        competitions=competitions
    )

@app.route('/add_result', methods=['POST'])
def add_result():
    data = request.get_json() or {}

    result = Result(
        competition_id=data["competition_id"],
        competitor_id=data["competitor_id"],
        time=data["time"],
    )

    db.session.add(result)
    db.session.commit()
    return jsonify({}), 201

@app.route('/filter_results', methods=['POST'])
def filter_results():
    data = request.get_json() or {}
    competition_id = data["competition_id"]
    cutoff_time = data["cutoff_time"]

    query = (
        db.session.query(Result, Competition, Competitor)
        .join(Competition, Result.competition_id == Competition.id)
        .join(Competitor, Result.competitor_id == Competitor.id)
        .filter(Result.time <= cutoff_time)
    )

    if competition_id != -1:
        query = query.filter(Result.competition_id == competition_id)

    filtered = query.order_by(Result.time.asc()).all()

    rows = [
        {
            "competitor": competitor.name,
            "competition": competition.name,
            "time": result.time,
        }
        for result, competition, competitor in filtered
    ]

    return jsonify(rows), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
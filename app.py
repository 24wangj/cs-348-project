
import datetime

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    state = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date)

    def __repr__(self):
        return f"<Competition {self.id}: {self.name}>"

@app.route('/')
def index():
    competitions = Competition.query.order_by(Competition.id.asc()).all()
    return render_template('index.html', competitions=competitions)


@app.route('/seed', methods=['GET', 'POST'])
def seed():
    db.session.query(Competition).delete()
    if Competition.query.count() == 0:
        db.session.add(Competition(name='Best in West Lafayette', city='French Lick', state='Indiana', date=datetime.date.today()))
        db.session.add(Competition(name='Holy Airball', city='Columbus', state='Ohio', date=datetime.date.today()))
        db.session.commit()

    if request.method == 'POST':
        total = Competition.query.count()
        return jsonify({"total": total})

    return 'Seed complete. Visit / to view competitions.'

@app.route('/add_comp', methods=['POST'])
def add_comp():
    data = request.get_json() or {}
    competition_date = datetime.datetime.strptime(data["date"], "%Y-%m-%d").date()
    competition = Competition(
        name=data["name"],
        city=data["city"],
        state=data["state"],
        date=competition_date,
    )
    db.session.add(competition)
    db.session.commit()
    return jsonify({
        "id": competition.id,
        "name": competition.name,
        "city": competition.city,
        "state": competition.state,
        "date": competition.date.isoformat() if competition.date else "",
    }), 201

@app.route('/delete_comp', methods=['DELETE'])
def delete_comp():
    data = request.get_json() or {}
    competition_id = data["id"]
    db.session.delete(db.session.query(Competition).filter(Competition.id == competition_id).first())
    db.session.commit()

    return jsonify({}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
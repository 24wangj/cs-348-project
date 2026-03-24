
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

    def __repr__(self):
        return f"<Competitor {self.id}: {self.name}>"

@app.route('/')
def index():
    competitors = Competitor.query.order_by(Competitor.id.asc()).all()
    return render_template('index.html', competitors=competitors)


@app.route('/seed', methods=['GET', 'POST'])
def seed():
    db.session.query(Competitor).delete()
    if Competitor.query.count() == 0:
        db.session.add(Competitor(name='Luke Carrot', city='West Lafayette', state='Indiana'))
        db.session.add(Competitor(name='Matty Hiroto Inaba', city='Columbus', state='Ohio'))
        db.session.add(Competitor(name='Lil Bro', city='Columbus', state='Indiana'))
        db.session.commit()

    if request.method == 'POST':
        total = Competitor.query.count()
        return jsonify({"total": total})

    return 'Seed complete. Visit / to view competitors.'

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

@app.route('/delete_competitor', methods=['DELETE'])
def delete_competitor():
    data = request.get_json() or {}
    competitor_id = data["id"]

    competitor = db.session.query(Competitor).filter(Competitor.id == competitor_id).first()
    db.session.delete(competitor)
    db.session.commit()

    return jsonify({}), 201

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
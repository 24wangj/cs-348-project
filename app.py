
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
        db.session.add(Competition(name='Best in West Lafayette', city='French Lick', state='Indiana'))
        db.session.add(Competition(name='Holy Airball', city='Columbus', state='Ohio'))
        db.session.commit()

    if request.method == 'POST':
        total = Competition.query.count()
        return jsonify({"total": total})

    return 'Seed complete. Visit / to view competitions.'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
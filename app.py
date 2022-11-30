import os
from datetime import datetime, timedelta
import pytz

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///backups.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Backup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Backup %r>' % self.id


@app.route("/")
def index():
    backups = []
    try:
        compare_date = datetime.now(pytz.timezone("Europe/Moscow")) - timedelta(hours=1)
        actual_backups = Backup.query.filter(Backup.date > compare_date).all()
        for element in actual_backups:
            str_time = element.date.strftime("%d-%m-%Y %H:%M:%S")
            backups.append({
                'date': str_time,
                'title': element.title
            })
    except:
        pass

    return render_template("index.html", backups=backups)


@app.route("/set_backup", methods=['GET'])
def set_backup():
    try:
        base_name = request.args.get('base')
        new_backup = Backup(title=base_name, date=datetime.now(pytz.timezone("Europe/Moscow")))

        db.session.add(new_backup)
        db.session.commit()
        return "success", 200
    except Exception as ex:
        return "fail: " + str(ex), 400


app.run(debug=False, host='0.0.0.0', port=5000)

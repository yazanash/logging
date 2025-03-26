from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite example:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'

# MySQL example:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@host/dbname'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define a Log model
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)


# Create tables
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def home():
    return "Welcome api"


@app.route('/logs', methods=['POST'])
def save_logs():
    try:
        incoming_logs = request.json.get('logs')
        if not incoming_logs:
            return jsonify({"error": "No logs found"}), 400

        # Save logs to the database
        for log_message in incoming_logs:
            log = Log(message=log_message["message"])
            db.session.add(log)
        db.session.commit()

        return jsonify({"message": "Logs saved successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

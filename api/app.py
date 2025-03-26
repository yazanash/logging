from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.keucjebazomvqrebmmde:dR#AHczv55RV4_!@aws-0-eu-central-1.pooler.supabase.com:6543/postgres?sslmode=require"
db = SQLAlchemy(app)


# Define a Log model
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.String(500), nullable=False)

# Create tables app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@remotehost.com/dbname'
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
            log = Log(message=log_message["message"],timestamp=log_message["timestamp"])
            db.session.add(log)
        db.session.commit()

        return jsonify({"message": "Logs saved successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

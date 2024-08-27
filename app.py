# from flask import Flask, render_template, request, jsonify
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # Configure the SQLite database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qrcode_data.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # Define the database model with the correct table name
# class QRCode(db.Model):
#     __tablename__ = 'test1'  # This should match your actual table name in the database
#     id = db.Column(db.Integer, primary_key=True)
#     qr_data = db.Column(db.String(255), unique=True, nullable=False)
#     name = db.Column(db.String(255), nullable=False)

# # Create the database if it does not exist
# with app.app_context():
#     db.create_all()

# # Route for the home page
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Route to handle QR code data
# @app.route('/check_qr', methods=['POST'])
# def check_qr():
#     # Get QR code data from the request
#     qr_data = request.json.get('qr_data')
#     print("QR code Data", qr_data)

#     # Query the database to check if the QR code data exists
#     test1 = QRCode.query.filter_by(name=qr_data).first()

#     print(test1)

#     if test1:
#         # If found, return the associated name and matched status
#         return jsonify({'matched': True, 'name': test1.name})
#     else:
#         # If not found, return not matched
#         return jsonify({'matched': False})

# if __name__ == '__main__':
#     app.run(debug=True)
import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the PostgreSQL database if on Heroku, otherwise use SQLite for local development
if 'DATABASE_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']  # Use Heroku's PostgreSQL database
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qrcode_data.db'  # Fallback for local development

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database model with the correct table name
class QRCode(db.Model):
    __tablename__ = 'test1'
    id = db.Column(db.Integer, primary_key=True)
    qr_data = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle QR code data
@app.route('/check_qr', methods=['POST'])
def check_qr():
    # Get QR code data from the request
    qr_data = request.json.get('qr_data')
    print("QR code Data", qr_data)

    # Query the database to check if the QR code data exists
    test1 = QRCode.query.filter_by(name=qr_data).first()

    print(test1)

    if test1:
        # If found, return the associated name and matched status
        return jsonify({'matched': True, 'name': test1.name})
    else:
        # If not found, return not matched
        return jsonify({'matched': False})

if __name__ == '__main__':
    app.run(debug=True)

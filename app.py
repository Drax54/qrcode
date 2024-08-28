import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env into the environment
from flask import abort

app = Flask(__name__)

# Configure the SQLite database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qrcode_data.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# Update the SQLALCHEMY_DATABASE_URI to use PostgreSQL

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:root@localhost/myproject')

database_url = os.getenv('DATABASE_URL')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

# # Define the database model
# class QRCode(db.Model):
#     __tablename__ = 'test2'  # Update this if your table name is actually 'test2'
#     id = db.Column(db.Integer, primary_key=True)
#     qr_data = db.Column(db.String(255), unique=True, nullable=False)
#     name = db.Column(db.String(255), nullable=False)
#     age = db.Column(db.Integer)  # Add this line to include the 'age' attribute

class QRCode(db.Model):
    __tablename__ = 'test2'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    paid = db.Column(db.Boolean, default=False)

def create_table():
    inspector = inspect(db.engine)
    if not inspector.has_table('test2', schema='public'):  # Adjust the schema if necessary
        db.create_all()
        print("Created table 'test2'")
    else:
        print("Table 'test2' already exists.")


with app.app_context():
    create_table()


# Create the database if it does not exist
with app.app_context():
    db.create_all()

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle submission

@app.route('/add-info', methods=['GET'])
def add_info():
    return render_template('add_info.html')

# Route to handle QR code data
@app.route('/check_qr', methods=['POST'])
def check_qr():
    # Get QR code data from the request
    qr_data = request.json.get('qr_data')
    print("QR code data:", qr_data)

    # Query the database to check if the name matches the qr_data
    test2 = QRCode.query.filter_by(name=qr_data).first()

    print(test2)

    if test2:
        # If found, return the associated name and matched status
        return jsonify({'matched': True, 'name': test2.name, 'age': test2.age})
    else:
        # If not found, return not matched
        return jsonify({'matched': False})
    
@app.route('/add-info', methods=['POST'])
def handle_info():
    try:
        name = request.form['name']
        age = request.form.get('age', type=int)
        paid = 'paid' in request.form  # Returns True if checkbox is checked

        # Create new QRCode entry
        new_entry = QRCode(name=name, age=age, paid=paid)
        db.session.add(new_entry)
        db.session.commit()

        return "Information submitted successfully!"
    except Exception as e:
        print(f"An error occurred: {e}")
        abort(500, description="An error occurred when submitting information.")


if __name__ == '__main__':
    app.run(debug=True)

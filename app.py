from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials

# Initialize Flask app
app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Change this to a secure key

# Initialize Firebase
cred = credentials.Certificate("C:/Users/lmaal/Downloads/basdb-20b5b-firebase-adminsdk-rg388-367ca2f721.json")
firebase_admin.initialize_app(cred)

from students import students_bp
from parents import parents_bp
from drivers import drivers_bp

app.register_blueprint(students_bp)
app.register_blueprint(parents_bp)
app.register_blueprint(drivers_bp)

# Define routes
@app.route('/')
def login_page():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)



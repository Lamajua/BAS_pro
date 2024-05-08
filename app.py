from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials




# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("/Users/maramnaif/Downloads/basdb-20b5b-firebase-adminsdk-rg388-cfcfa1930f.json")
firebase_admin.initialize_app(cred)

from students import students_bp
from parents import parents_bp
from drivers import drivers_bp
from buses import buses_bp


app.register_blueprint(students_bp)
app.register_blueprint(parents_bp)
app.register_blueprint(drivers_bp)
app.register_blueprint(buses_bp)


# Define routess
@app.route('/')
def login_page():
    return render_template('login.html')


    
if __name__ == '__main__':
    app.run(debug=True)


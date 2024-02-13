from flask import Blueprint, render_template, request, redirect
from firebase_admin import firestore

drivers_bp = Blueprint('drivers', __name__)
db = firestore.client()

@drivers_bp.route('/drivers')
def drivers():
    drivers = db.collection('drivers').get()
    return render_template('drivers.html', drivers=drivers)


@drivers_bp.route('/add_driver', methods=['POST'])
def add_driver():
    name = request.form['name']
    phone_number = request.form['phone_number']
    licenseExpDate = request.form['licExpDt']
    bus_number = request.form['bus_number']

    drivers_data = {
        'name': name,
        'phone_number': phone_number,
        'licExpDt': licenseExpDate,
        'bus_number': bus_number
    }

    db.collection('drivers').add(drivers_data)
    return redirect('/drivers')


@drivers_bp.route('/edit_driver/<string:driver_id>', methods=['POST'])
def edit_driver(driver_id):
    name = request.form['name']
    phone_number = request.form['phone_number']
    licenseExpDate = request.form['licExpDt']
    bus_number = request.form['bus_number']

    db.collection('drivers').document(driver_id).update({
        'name': name,
        'phone_number': phone_number,
        'licExpDt': licenseExpDate,
        'bus_number': bus_number
    })

    return redirect('/drivers')

@drivers_bp.route('/delete_driver/<string:driver_id>', methods=['POST'])
def delete_driver(driver_id):
    db.collection('drivers').document(driver_id).delete()
    return redirect('/drivers')
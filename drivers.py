from firebase_admin import firestore, auth
from flask import request, render_template, redirect, url_for
from flask import Blueprint, render_template, request, redirect
from flask import request, render_template, redirect, url_for
from flask import request


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
    password = request.form['password']
    firebase_uid = "1"

    # Check if the driver already exist by checking the phone number
    existing_driver = db.collection('drivers').where('phone_number', '==', phone_number).get()
    if existing_driver:
        error_message = "Phone number already exists for another driver."
        drivers = db.collection('drivers').get()
        return render_template('drivers.html', drivers=drivers, error=error_message)

    try:
        driver_ref = db.collection('drivers').add({
            'name': name,
            'phone_number': phone_number,
            'licExpDt': licenseExpDate,
            'bus_number': bus_number,
            'firebase_uid' : firebase_uid,
            'user_type' : 'driver',
        })

        driver_id = driver_ref[1].id

        # Create a user in firebase (auth service)
        user = auth.create_user(
            email=phone_number + '@bas.com',
            password=password
        )
        print('Successfully created new user: {0}'.format(user.uid))

        # Update firestore db with the user id of the driver
        db.collection('drivers').document(driver_id).update({
            'firebase_uid': user.uid
        })

    except Exception as e:
        print('Error creating driver:', e)
        return redirect('/drivers?error=true')

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
  

@drivers_bp.route('/drivers', methods=['GET', 'POST'])
def show_drivers():
    if request.method == 'POST':
        # Handle search functionality if a POST request is received
        search_query = request.form.get('search_query', '')

        drivers_query = db.collection('drivers')

        if search_query:
            drivers_query = drivers_query.where('phone_number', '>=', search_query).where('phone_number', '<=', search_query + u'\uf8ff')

        drivers = drivers_query.get()

        return render_template('drivers.html', drivers=drivers, search_query=search_query)
    else:
        # Handle displaying all drivers when a GET request is received
        drivers = db.collection('drivers').get()
        return render_template('drivers.html', drivers=drivers)

@drivers_bp.route('/clear_search', methods=['POST'])
def clear_search():
    return redirect(url_for('drivers.show_drivers'))


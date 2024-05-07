from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from firebase_admin import firestore, auth
from flask import request, render_template, redirect, url_for

parents_bp = Blueprint('parents', __name__)
db = firestore.client()


@parents_bp.route('/parents')
def parents():
    parents = db.collection('parents').get()
    students = db.collection('students').get()
    return render_template('parents.html', parents=parents, students=students)


@parents_bp.route('/add_parent', methods=['POST'])
def add_parent():
    name = request.form['name']
    phone_number = request.form['phone_number']
    password = request.form['password']
    address = request.form['address']
    #latitude = float(request.form['latitude'])
    #longitude = float(request.form['longitude'])
    students = []
    firebase_uid = "1"

    student_keys = [key for key in request.form.keys() if key.startswith('student_name')]
    for key in student_keys:
        index = key.split('_')[-1]
        student_name = request.form[f'student_name_{index}']
        bus_number = request.form[f'bus_number_{index}']
        students.append({
            'name': student_name,
            'bus_number': bus_number,
            'parent_phone_number': phone_number,
            'status_pickup': 'present',
            'status_dropoff': 'present',
            #'latitude': latitude,
            #'longitude': longitude
        })

    # Check if the bus number and district exist in the buses table
    bus_query = db.collection('buses').where('number', '==', bus_number).where('district', '==', address).get()
    if not bus_query:
        error_message = "The provided Bus number and Address do not match any existing record."
        parents = db.collection('parents').get()
        return render_template('parents.html', parents=parents, error=error_message)

    # Check if the parent's phone number already exists
    existing_parent = db.collection('parents').where('phone_number', '==', phone_number).get()
    if existing_parent:
        error_message = "Phone number already exists for another parent."
        parents = db.collection('parents').get()
        return render_template('parents.html', parents=parents, error=error_message)

    try:
        parent_ref = db.collection('parents').add({
            'name': name,
            'phone_number': phone_number,
            'address': address,
           # 'latitude': latitude,
           # 'longitude': longitude,
            'firebase_uid': firebase_uid,
            'user_type': 'parent',
        })


        parent_id = parent_ref[1].id

        for student_data in students:
            db.collection('students').add(student_data)

        user = auth.create_user(
            email=phone_number + '@bas.com',
            password=password
        )
        print('Successfully created new user: {0}'.format(user.uid))

        db.collection('parents').document(parent_id).update({
            'firebase_uid': user.uid
        })

    except Exception as e:
        print('Error creating parent:', e)
        return redirect('/parents?error=true')

    return redirect('/parents')


@parents_bp.route('/edit_parent/<string:parent_id>', methods=['POST'])
def edit_parent(parent_id):
    name = request.form['name']
    address = request.form['address']
    #latitude = request.form['latitude']
    #longitude = request.form['longitude']

    # Update parent information
    db.collection('parents').document(parent_id).update({
        'name': name,
        'address': address,
        #'latitude': latitude,
        #'longitude': longitude,
    })

    # Update child (student) information
    for key, value in request.form.items():
        if key.startswith('student_name_'):
            student_id = key.split('_')[-1]
            db.collection('students').document(student_id).update({
                'name': value
            })
        elif key.startswith('bus_number_'):
            student_id = key.split('_')[-1]
            db.collection('students').document(student_id).update({
                'bus_number': value
            })

    return redirect('/parents')





@parents_bp.route('/get_students_by_parent_phone/<string:parent_id>')
def get_students_by_parent_phone(parent_id):
    parent_phone_number = db.collection('parents').document(
        parent_id).get().to_dict()['phone_number']
    students = db.collection('students').where(
        'parent_phone_number', '==', parent_phone_number).get()
    student_data = [{'name': student.to_dict()['name'], 'bus_number': student.to_dict()[
        'bus_number']} for student in students]
    return jsonify(student_data)


@parents_bp.route('/delete_parent/<string:parent_id>', methods=['POST'])
def delete_parent(parent_id):
    parent_ref = db.collection('parents').document(parent_id)
    parent_data = parent_ref.get().to_dict()

    # Delete parent
    parent_ref.delete()

    # Delete all students with the same phone number
    students = db.collection('students').where(
        'parent_phone_number', '==', parent_data['phone_number']).get()
    for student in students:
        db.collection('students').document(student.id).delete()

    return redirect('/parents')


    
@parents_bp.route('/deactivate_parent/<string:parent_id>', methods=['POST'])
def deactivate_parent(parent_id):
    try:
        # Update the parent in firestore db to True in deactivated
        db.collection('parents').document(parent_id).update({
            'deactivated': True
        })
    except Exception as e:
        print('Error deactivating parent:', e)
        return redirect('/parents?error=true')

    return redirect('/parents')

@parents_bp.route('/activate_parent/<string:parent_id>', methods=['POST'])
def activate_parent(parent_id):
    try:
        # Update the parent in Firestore to set 'deactivated' field to False
        db.collection('parents').document(parent_id).update({
            'deactivated': False
        })
    except Exception as e:
        print('Error activating parent:', e)
        return redirect('/parents?error=true')

    return redirect('/parents')


    # Search bar
@parents_bp.route('/parents', methods=['GET', 'POST'])
def show_parents():
    if request.method == 'POST':
        # Handle search functionality if a POST request is received
        search_query = request.form.get('search_query', '')

        parents_query = db.collection('parents')

        if search_query:
            parents_query = parents_query.where('phone_number', '>=', search_query).where(
                'phone_number', '<=', search_query + u'\uf8ff')

        parents = parents_query.get()

        return render_template('parents.html', parents=parents, search_query=search_query)
    else:
        # Handle displaying all parents when a GET request is received
        parents = db.collection('parents').get()
        return render_template('parents.html', parents=parents)


@parents_bp.route('/clear_search', methods=['POST'])
def clear_search():
    return redirect(url_for('parents.show_parents'))

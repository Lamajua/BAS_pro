from flask import Blueprint, jsonify, render_template, request, redirect
from firebase_admin import firestore, auth
import firebase_admin

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
    students = []

    student_keys = [key for key in request.form.keys() if key.startswith('student_name')]
    for key in student_keys:
        index = key.split('_')[-1]
        student_name = request.form[f'student_name_{index}']
        bus_number = request.form[f'bus_number_{index}']
        students.append({
            'name': student_name,
            'bus_number': bus_number,
            'parent_phone_number': phone_number 
        })


    existing_parent = db.collection('parents').where('phone_number', '==', phone_number).get()
    if existing_parent:
        error_message = "Phone number already exists for another parent."
        parents = db.collection('parents').get()
        return render_template('parents.html', parents=parents, error=error_message)


    try:
        parent_ref, parent_id = db.collection('parents').add({
            'name': name,
            'phone_number': phone_number,
            'address' : address,
        })

        for student_data in students:
            db.collection('students').add(student_data)

        # Create a user account in Firebase Authentication
        user = auth.create_user(
            email=phone_number + '@example.com',
            password=password
        )
        print('Successfully created new user: {0}'.format(user.uid))

        # Update Firestore to store the Firebase UID of the parent user
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

    db.collection('parents').document(parent_id).update({
        'name': name,
        'address': address,
    })

    return redirect('/parents')

@parents_bp.route('/get_students_by_parent_phone/<string:parent_id>')
def get_students_by_parent_phone(parent_id):
    parent_phone_number = db.collection('parents').document(parent_id).get().to_dict()['phone_number']
    students = db.collection('students').where('parent_phone_number', '==', parent_phone_number).get()
    student_data = [{'name': student.to_dict()['name'], 'bus_number': student.to_dict()['bus_number']} for student in students]
    return jsonify(student_data)


@parents_bp.route('/delete_parent/<string:parent_id>', methods=['POST'])
def delete_parent(parent_id):
    parent_ref = db.collection('parents').document(parent_id)
    parent_data = parent_ref.get().to_dict()

    # Delete parent
    parent_ref.delete()

    # Delete all students with the same phone number as the deleted parent
    students = db.collection('students').where('parent_phone_number', '==', parent_data['phone_number']).get()
    for student in students:
        db.collection('students').document(student.id).delete()

    return redirect('/parents')



@parents_bp.route('/deactivate_parent/<string:parent_id>', methods=['POST'])
def deactivate_parent(parent_id):
    try:
        # Update the parent document in Firestore to set the 'deactivated' field to True
        db.collection('parents').document(parent_id).update({
            'deactivated': True
        })
    except Exception as e:
        print('Error deactivating parent:', e)
        return redirect('/parents?error=true')  # Redirect with error parameter

    return redirect('/parents')

from flask import Blueprint, render_template, request, redirect
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
    student_name = request.form['student_name']
    student_address = request.form['student_address']
    bus_number = request.form['bus_number']

    # Check if the phone number already exists for another parent
    existing_parent = db.collection('parents').where('phone_number', '==', phone_number).get()
    if existing_parent:
        # Phone number already exists, show error message
        error_message = "Phone number already exists for another parent."
        parents = db.collection('parents').get()
        return render_template('parents.html', parents=parents, error=error_message)


    parents_data = {
        'name': name,
        'phone_number': phone_number,
    }

    try:
        # Add parent data to Firestore
        parent_ref, parent_id = db.collection('parents').add(parents_data)

        # Add student data to Firestore
        student_data = {
            'name': student_name,
            'address': student_address,
            'bus_number': bus_number,
            'parent_phone_number': phone_number  # Link student to parent using parent's phone number
        }
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
        return redirect('/parents?error=true')  # Redirect with error parameter

    return redirect('/parents')



    # name = request.form['name']
    # phone_number = request.form['phone_number']
    # password = request.form['password'] 

    # existing_parent = db.collection('parents').where('phone_number', '==', phone_number).get()
    # if existing_parent:
    #     # Phone number already exists, show error message
    #     error_message = "Phone number already exists for another parent."
    #     parents = db.collection('parents').get()
    #     return render_template('parents.html', parents=parents, error=error_message)

    # parents_data = {
    #     'name': name,
    #     'phone_number': phone_number,
    # }

    # try:
    #     # Add parent data to Firestore
    #     parent_ref, parent_id = db.collection('parents').add(parents_data)
    #     print("Parent reference:", parent_ref)
    #     print("Parent ID:", parent_id)

    #     # Create a user account in Firebase Authentication
    #     user = auth.create_user(
    #         email=phone_number + '@example.com',
    #         password=password
    #     )
    #     print('Successfully created new user: {0}'.format(user.uid))

    #     # Update Firestore to store the Firebase UID of the parent user
    #     db.collection('parents').document(parent_id).update({
    #         'firebase_uid': user.uid
    #     })

    # except Exception as e:
    #     print('Error creating parent:', e)
    #     return redirect('/parents?error=true')  # Redirect with error parameter

    # return redirect('/parents')


@parents_bp.route('/edit_parent/<string:parent_id>', methods=['POST'])
def edit_parent(parent_id):
    name = request.form['name']
    phone_number = request.form['phone_number']

    db.collection('parents').document(parent_id).update({
        'name': name,
        'phone_number': phone_number,
    })

    return redirect('/parents')


@parents_bp.route('/delete_parent/<string:parent_id>', methods=['POST'])
def delete_parent(parent_id):
    db.collection('parents').document(parent_id).delete()
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

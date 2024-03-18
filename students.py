from flask import Blueprint, render_template, request, redirect
from firebase_admin import firestore
from flask import request, render_template, redirect, url_for


students_bp = Blueprint('students', __name__)
db = firestore.client()

@students_bp.route('/students', methods=['GET', 'POST'])
def show_students():
    if request.method == 'POST':
        search_query = request.form['search_query']
        if search_query:
            students = db.collection('students').where('name', '==', search_query).get()
        else:
            students = db.collection('students').get()
    else:
        students = db.collection('students').get()
        
    parents = db.collection('parents').get()
    return render_template('students.html', students=students, parents=parents)

@students_bp.route('/clear_search', methods=['POST'])
def clear_search():
    return redirect(url_for('students.show_students'))



@students_bp.route('/students')
def students():
    students = db.collection('students').get()
    parents = db.collection('parents').get()
    return render_template('students.html', students=students, parents=parents)

@students_bp.route('/edit_student/<string:student_id>', methods=['POST'])
def edit_student(student_id):
    name = request.form['name']
    address = request.form['address']
    bus_number = request.form['bus_number']
    
    

    db.collection('students').document(student_id).update({
        'name': name,
        'address': address,
        'bus_number': bus_number
    })

    return redirect('/students')

@students_bp.route('/delete_student/<string:student_id>', methods=['POST'])
def delete_student(student_id):
    db.collection('students').document(student_id).delete()
    return redirect('/students')


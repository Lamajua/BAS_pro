from flask import Blueprint, render_template, request, redirect
from firebase_admin import firestore

buses_bp = Blueprint("buses", __name__)
db = firestore.client()


@buses_bp.route("/buses")
def buses():
    buses = db.collection("buses").get()
    return render_template("buses.html", buses=buses)


@buses_bp.route("/add_bus", methods=["POST"])
def add_bus():
    number = request.form["number"]
    district = request.form["district"]
   

    buses_data = {
        "number": number,
        "district": district,
    }

    db.collection("buses").add(buses_data)
    return redirect("/buses")


@buses_bp.route("/edit_bus/<string:bus_id>", methods=["POST"])
def edit_bus(bus_id):
    number = request.form["number"]
    district = request.form["district"]

    db.collection("buses").document(bus_id).update(
        {
        "number": number, 
        "district": district, 
        }
    )

    return redirect("/buses")


@buses_bp.route("/delete_bus/<string:bus_id>", methods=["POST"])
def delete_bus(bus_id):
    db.collection("buses").document(bus_id).delete()
    return redirect("/buses")

import db_config as db
from random import randint
from app import create_app
from bson.json_util import dumps
from flask_pymongo import pymongo
from flask_cors import CORS
from flask import jsonify, request, render_template, redirect

app = create_app()
CORS(app)

@app.route("/")
def inicio():
    place = dict(db.db.BeforeDie.find_one({"name" : "Hawaii"}))
    all_places = list(db.db.BeforeDie.find())
    return render_template('index.html', lugar = place, lugares = all_places)

@app.route("/place/<string:name>")
def places(name):
    place = dict(db.db.BeforeDie.find_one({"name" : name}))
    all_places = list(db.db.BeforeDie.find())
    themes = randint(1, 10)
    return render_template('index.html', lugar = place, lugares = all_places, temas = themes)

@app.route("/places/newPlace/<string:name>", methods = ['POST'])
def new_place(name):
    if len(request.json) == 3:
        db.db.BeforeDie.insert_one({
            "name" : request.json["name"],
            "coordinates" : request.json["coordinates"],
            "description" : request.json["description"],
        })
    else:
        return jsonify({
            "error" : "¡Faltan datos!",
        })
    return jsonify({
        "status" : 200,
        "message" : f"El lugar {request.json['name']} ha sido añadido"
    })

@app.route("/places/showPlaces/")
def test():
    place = dumps(db.db.BeforeDie.find())
    return place

@app.route("/places/showOne/<string:name>")
def testOne(name):
    place = dumps(db.db.BeforeDie.find_one({"name" : name}))
    return place

@app.route("/places/deletePlace/<string:name>", methods = ['DELETE'])
def delete_place(name):
    if db.db.BeforeDie.find_one({"name" : name}):
        db.db.BeforeDie.delete_one({"name" : name})
    else:
        return jsonify({
            "error" : 400,
            "message" : f"El lugar {name} no ha sido encontrada :(",
        })
    return jsonify({
        "status" : 200,
        "message" : f"El lugar {name} ha sido eliminada"
    })

if __name__ == "__main__":
    app.run(load_dotenv=True, port=3030)

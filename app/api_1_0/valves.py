from flask import jsonify, request
from . import api
from ..models import Valve, valve_schema, valves_schema
from .. import db


@api.route("/valve/<int:id>")
def get_valve(id):
    valve = Valve.query.get(id)
    return valve_schema.jsonify(valve)


@api.route("/valve")
def get_valves():
    all_valves = Valve.query.all()
    result = valves_schema.dump(all_valves)
    return jsonify(result.data)


@api.route("/valve", methods=["POST"])
def add_valve():
    tag = request.json['tag']
    size = request.json['size']
    new_valve = Valve(tag, size)
    db.session.add(new_valve)
    db.session.commit()
    return jsonify(new_valve)


@api.route("/valve/<int:id>", methods=["PUT"])
def valve_update(id):
    valve = Valve.query.get(id)
    tag = request.json['tag']
    size = request.json['size']
    valve.tag = tag
    valve.size = size
    db.session.commit()
    return valve_schema.jsonify(valve)


@api.route("/valve/<int:id>", methods=["DELETE"])
def valve_delete(id):
    valve = Valve.query.get(id)
    db.session.delete(valve)
    db.session.commit()
    return valve_schema.jsonify(valve)

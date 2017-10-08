from flask import jsonify, request, url_for, g
from . import api
from ..models import Valve, Log
from .. import db


@api.route("/valves/")
def get_valves():
    valves = Valve.query.all()
    return jsonify({
        'valves': [valve.to_json() for valve in valves]
    })


@api.route("/valves/<int:id>")
def get_valve(id):
    valve = Valve.query.get_or_404(id)
    return jsonify(valve.to_json())


@api.route("/valves/", methods=["POST"])
def new_valve():
    valve = Valve.from_json(request.json)
    db.session.add(valve)
    db.session.commit()
    return jsonify(valve.to_json()), 201


@api.route("/valves/<int:id>", methods=["PUT"])
def valve_update(id):
    valve = Valve.query.get_or_404(id)
    tag = request.json['tag']
    size = request.json['size']
    valve.tag = tag
    valve.size = size
    db.session.commit()
    return jsonify(valve.to_json())


@api.route("/valves/<int:id>", methods=["DELETE"])
def valve_delete(id):
    valve = Valve.query.get_or_404(id)
    db.session.delete(valve)
    db.session.commit()
    return jsonify(valve.to_json())

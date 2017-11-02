from flask import jsonify, request, url_for, g
from . import api
from ..models import Valve, Log
from .. import db


@api.route("/valves/", methods=['GET'])
def get_valves():
    return jsonify({
        'valves': [valve.get_url() for valve in Valve.query.all()]
    })


@api.route("/valves/<int:id>", methods=['GET'])
def get_valve(id):
    return jsonify(Valve.query.get_or_404(id).export_data())


@api.route("/valves/", methods=["POST"])
def new_valve():
    valve = Valve()
    valve.import_data(request.json)
    db.session.add(valve)
    db.session.commit()
    return jsonify({}), 201, {'Location': valve.get_url()}


@api.route("/valves/<int:id>", methods=["PUT"])
def edit_valve(id):
    valve = Valve.query.get_or_404(id)
    valve.import_data(request.json)
    db.session.add(valve)
    db.session.commit()
    return jsonify({})


@api.route("/valves/<int:id>", methods=["DELETE"])
def valve_delete(id):
    valve = Valve.query.get_or_404(id)
    db.session.delete(valve)
    db.session.commit()
    return jsonify({})

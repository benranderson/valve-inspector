from flask import jsonify, request, abort, url_for, g
from . import api
from ..models import Valve, Log
from .. import db


@api.route('/logs/')
def get_logs():
    logs = Log.query.order_by(Log.time.desc())
    return jsonify({
        'logs': [log.to_json() for log in logs],
    })


@api.route('/logs/<int:id>')
def get_log(id):
    log = Log.query.get_or_404(id)
    return jsonify(log.to_json())


@api.route('/valves/<int:id>/logs/')
def get_valve_logs(id):
    valve = Valve.query.get_or_404(id)
    logs = valve.logs.order_by(Log.time.asc())
    return jsonify({
        'logs': [log.to_json() for log in logs],
    })


@api.route('/valves/<int:id>/logs', methods=['POST'])
def new_valve_log(id):
    valve = Valve.query.get_or_404(id)
    log = Log.from_json(request.json)
    log.valve = valve
    db.session.add(log)
    db.session.commit()
    return jsonify(log.to_json()), 201

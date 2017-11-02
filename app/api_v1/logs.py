from flask import jsonify, request, g
from . import api
from .. import db
from ..models import Valve, Log


@api.route('/logs/', methods=['GET'])
def get_logs():
    return jsonify({
        'logs': [log.get_url() for log in Log.query.order_by(Log.date.desc())]
    })


@api.route('/valves/<int:id>/logs/', methods=['GET'])
def get_valve_logs(id):
    valve = Valve.query.get_or_404(id)
    return jsonify({
        'logs': [log.get_url() for log in valve.logs.all()]
    })


@api.route('/logs/<int:id>', methods=['GET'])
def get_log(id):
    log = Log.query.get_or_404(id)
    return jsonify({Log.query.get_or_404(id).export_data()})


@api.route('/valves/<int:id>/logs', methods=['POST'])
def new_valve_log(id):
    valve = Valve.query.get_or_404(id)
    log = Log(valve=valve)
    log.import_data(request.json)
    db.session.add(log)
    db.session.commit()
    return jsonify({}), 201, {'Location': log.get_url()}


@api.route('/logs/<int:id>', methods=['PUT'])
def edit_log(id):
    log = Log.query.get_or_404(id)
    log.import_data(request.json)
    db.session.add(log)
    db.session.commit()
    return jsonify({})


@api.route('/logs/<int:id>', methods=['DELETE'])
def delete_log(id):
    log = Log.query.get_or_404(id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({})

from flask import jsonify, request
from . import api
from ..models import Project, Valve
from .. import db


@api.route("/projects/", methods=['GET'])
def get_projects():
    return jsonify({
        'projects': [projects.get_url() for projects in Project.query.all()]
    })


@api.route("/projects/<int:id>", methods=['GET'])
def get_project(id):
    return jsonify(Project.query.get_or_404(id).export_data())


# @api.route("/valves/", methods=["POST"])
# def new_valve():
#     valve = Valve()
#     valve.import_data(request.json)
#     db.session.add(valve)
#     db.session.commit()
#     return jsonify({}), 201, {'Location': valve.get_url()}


# @api.route("/valves/<int:id>", methods=["PUT"])
# def edit_valve(id):
#     valve = Valve.query.get_or_404(id)
#     valve.import_data(request.json)
#     db.session.add(valve)
#     db.session.commit()
#     return jsonify({})


# @api.route("/valves/<int:id>", methods=["DELETE"])
# def valve_delete(id):
#     valve = Valve.query.get_or_404(id)
#     db.session.delete(valve)
#     db.session.commit()
#     return jsonify({})

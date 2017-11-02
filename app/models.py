from datetime import datetime
from dateutil import parser as datetime_parser
from dateutil.tz import tzutc
from flask import url_for
from . import db
from .exceptions import ValidationError


class ValidationError(ValueError):
    pass


class Valve(db.Model):

    __tablename__ = 'valves'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String, nullable=False, index=True, unique=True)
    size = db.Column(db.Integer)
    logs = db.relationship('Log', backref='valve', lazy='dynamic')

    def __repr__(self):
        return '<Valve {}>'.format(self.tag)

    def get_url(self):
        return url_for('api.get_valve', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'tag': self.tag,
            'size': self.size,
            'logs': url_for('api.get_valve_logs', id=self.id, _external=True),
            'log_count': self.logs.count(),
        }

    def import_data(self, data):
        try:
            self.tag = data['tag']
            self.size = data['size']
        except KeyError as e:
            raise ValidationError('Invalid valve: missing ' + e.args[0])
        return self


class Log(db.Model):

    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    valve_id = db.Column(db.Integer, db.ForeignKey('valves.id'), index=True)
    status = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Log {}>'.format(self.status)

    def get_url(self):
        return url_for('api.get_log', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'valve_url': self.valve.get_url(),
            'date':  self.date.isoformat() + 'Z',
            'status': self.status,
        }

    def import_data(self, data):
        try:
            self.date = datetime_parser.parse(data['date']).astimezone(
                tzutc()).replace(tzinfo=None)
        except KeyError as e:
            raise ValidationError('Invalid log: missing ' + e.args[0])
        return self

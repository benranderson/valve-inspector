from flask import url_for
import datetime as dt
from app.exceptions import ValidationError
from app import db, ma


class ValidationError(ValueError):
    pass


class Valve(db.Model):

    __tablename__ = 'valves'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String, nullable=False)
    size = db.Column(db.Float, nullable=False)
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
        except KeyError as e:
            raise ValidationError('Invalid tag')
        try:
            self.size = data['size']
        except KeyError as e:
            raise ValidationError('Invalid size')
        return self


class Log(db.Model):

    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Date, nullable=False, default=dt.datetime.now())
    status = db.Column(db.String, nullable=False)
    valve_id = db.Column(db.Integer, db.ForeignKey('valves.id'))

    def __repr__(self):
        return '<Log {}>'.format(self.status)

    def get_url(self):
        return url_for('api.get_log', id=self.id, _external=True)

    def to_json(self):
        return {
            'url': self.get_url(),
            'valve': url_for('api.get_valve', id=self.valve_id, _external=True),
            'time': self.time,
            'status': self.status,
        }

    def import_data(self, data):
        try:
            self.time = dt.datetime.strptime(
                data['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except KeyError as e:
            raise ValidationError('Invalid time')
        try:
            self.status = data['status']
        except KeyError as e:
            raise ValidationError('Invalid status')
        return self

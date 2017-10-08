from flask import url_for
import datetime as dt
from app.exceptions import ValidationError
from app import db, ma


class Valve(db.Model):

    __tablename__ = 'valves'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String, nullable=False)
    size = db.Column(db.Float, nullable=False)
    logs = db.relationship('Log', backref='valve', lazy='dynamic')

    def __repr__(self):
        return '<Valve {}>'.format(self.tag)

    def to_json(self):
        json_valve = {
            'url': url_for('api.get_valve', id=self.id, _external=True),
            'tag': self.tag,
            'size': self.size,
            'logs': url_for('api.get_valve_logs', id=self.id, _external=True),
            'log_count': self.logs.count(),
        }
        return json_valve

    @staticmethod
    def from_json(json_valve):
        tag = json_valve.get('tag')
        size = json_valve.get('size')
        if tag is None or tag == '':
            raise ValidationError('valve does not have a tag')
        if size is None or size == '':
            raise ValidationError('valve does not have a size')
        return Valve(tag=tag, size=size)


class Log(db.Model):

    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Date, nullable=False, default=dt.datetime.now())
    status = db.Column(db.String, nullable=False)
    valve_id = db.Column(db.Integer, db.ForeignKey('valves.id'))

    def __repr__(self):
        return '<Log {}>'.format(self.status)

    def to_json(self):
        json_log = {
            'url': url_for('api.get_log', id=self.id, _external=True),
            'valve': url_for('api.get_valve', id=self.valve_id, _external=True),
            'time': self.time,
            'status': self.status,
        }
        return json_log

    @staticmethod
    def from_json(json_log):
        time = dt.datetime.strptime(
            json_log.get('time'), '%Y-%m-%dT%H:%M:%S.%fZ')
        status = json_log.get('status')
        # if time is None or time == '':
        #     raise ValidationError('log does not have a time')
        return Log(time=time, status=status)

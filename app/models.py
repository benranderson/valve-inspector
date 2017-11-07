from datetime import datetime
from dateutil import parser as datetime_parser
from dateutil.tz import tzutc
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from . import db, login_manager, admin
from .exceptions import ValidationError

class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role {}>'.format(self.name)

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Valve(db.Model):

    __tablename__ = 'valves'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64), nullable=False, index=True, unique=True)
    size = db.Column(db.Integer)
    location = db.Column(db.String(64))
    logs = db.relationship('Log', backref='valve', lazy='dynamic')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), index=True)

    def __repr__(self):
        return '<Valve {}>'.format(self.tag)

    def get_url(self):
        return url_for('api.get_valve', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'tag': self.tag,
            'size': self.size,
            'location': self.location,
            'logs': url_for('api.get_valve_logs', id=self.id, _external=True),
            'log_count': self.logs.count(),
        }

    def import_data(self, data):
        try:
            self.tag = data['tag']
            self.size = data['size']
            self.location = data['location']
        except KeyError as e:
            raise ValidationError('Invalid valve: missing ' + e.args[0])
        return self

    @property
    def status(self):
        if len(self.logs.all()) > 0:
            return self.logs.all()[-1].status
        else:
            return "No status logged"


class Log(db.Model):

    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(6), nullable=False)
    turns = db.Column(db.Float)
    valve_id = db.Column(db.Integer, db.ForeignKey('valves.id'), index=True)

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
            'turns': self.turns,
        }

    def import_data(self, data):
        try:
            self.date = datetime_parser.parse(data['date']).astimezone(
                tzutc()).replace(tzinfo=None)
            self.status = data['status']
            self.turns = data['turns']
        except KeyError as e:
            raise ValidationError('Invalid log: missing ' + e.args[0])
        return self

class Project(db.Model):

    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(128), index=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    client = db.Column(db.String(128))
    vessel = db.Column(db.String(128))
    campaign = db.Column(db.String(128))
    date = db.Column(db.DateTime)
    valves = db.relationship('Valve', backref='project', lazy='dynamic')

    def __repr__(self):
        return '<Project {}>'.format(self.number)

    def get_url(self):
        return url_for('api.get_project', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'number':  self.number,
            'title': self.title,
            'client': self.client,
            'vessel': self.vessel,
            'campaign': self.campaign,
            'date': self.date.isoformat() + 'Z',
            'valves': url_for('api.get_project', id=self.id, _external=True),
        }

    def import_data(self, data):
        try:
            self.number = data['number']
            self.title = data['title']
            self.client = data['client']
            self.vessel = data['vessel']
            self.campaign = data['campaign']
            self.date = datetime_parser.parse(data['date']).astimezone(
                tzutc()).replace(tzinfo=None)
        except KeyError as e:
            raise ValidationError('Invalid project: missing ' + e.args[0])
        return self

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Valve, db.session))
admin.add_view(ModelView(Log, db.session))
admin.add_view(ModelView(Project, db.session))
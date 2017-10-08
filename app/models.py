import datetime as dt
from app import db, ma


class Valve(db.Model):

    __tablename__ = 'valves'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(5), nullable=False)
    size = db.Column(db.Float, nullable=False)
    logs = db.relationship('Log', backref='valve')

    def __init__(self, tag, size):
        self.tag = tag
        self.size = size

    def __repr__(self):
        return '<Valve {}>'.format(self.tag)

    # @property
    # def current_status(self):
    #     return self.status_log[-1]

    # def to_json(self):
    #     json_valve = {
    #         'tag': self.tag,
    #         'size': self.size,
    #         'status_log': self.status_log,
    #     }
    #     return json_valve


class ValveSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('tag', 'size')


valve_schema = ValveSchema()
valves_schema = ValveSchema(many=True)


class Log(db.Model):

    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Date, nullable=False)
    status = db.Column(db.String, nullable=False)
    valve_id = db.Column(db.Integer, db.ForeignKey('valves.id'))

    def __init__(self, status):
        self.time = dt.datetime.now()
        self.status = status

    def __repr__(self):
        return '<Log {}>'.format(self.status)


class LogSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('time', 'status')


log_schema = LogSchema()
logs_schema = LogSchema(many=True)

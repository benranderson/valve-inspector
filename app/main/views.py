from flask import request, render_template, url_for, redirect, Response

from app.main import main
from app.main.forms import ValveForm, LogForm
from app import db
from app.models import Valve, Log


@main.route('/', methods=['GET', 'POST'])
def index():
    form = ValveForm()
    if form.validate_on_submit():
        valve = Valve(tag=form.tag.data, size=form.size.data)
        db.session.add(valve)
        return redirect(url_for('.index'))
    valves = Valve.query.all()
    return render_template('index.html', form=form, valves=valves)


@main.route('/valve/<tag>', methods=['GET', 'POST'])
def valve(tag):
    form = LogForm()
    valve = Valve.query.filter_by(tag=tag).first()
    if form.validate_on_submit():
        log = Log(time=form.time.data, status=form.status.data)
        log.valve = valve
        db.session.add(log)
        return redirect(url_for('.valve', tag=tag))
    logs = valve.logs
    current_status = logs[-1].status
    return render_template('valve.html', form=form, valve=valve, logs=logs,
                           current_status=current_status)

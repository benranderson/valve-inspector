from flask import request, render_template, url_for, redirect, Response, flash
from app.main import main
from app.main.forms import ValveForm, LogForm
from app import db
from app.models import Valve, Log


@main.route('/', methods=['GET', 'POST'])
def index():
    form = ValveForm()
    if form.validate_on_submit():
        valve = Valve(tag=form.tag.data, size=form.size.data,
                      location=form.location.data)
        db.session.add(valve)
        flash('Valve added.')
        return redirect(url_for('.index'))
    valves = Valve.query.all()
    return render_template('index.html', form=form, valves=valves)


@main.route('/valve/<tag>', methods=['GET', 'POST'])
def valve(tag):
    valve = Valve.query.filter_by(tag=tag).first()
    form = LogForm()
    if form.validate_on_submit():
        log = Log(date=form.date.data, status=form.status.data,
                  turns=form.turns.data)
        log.valve = valve
        db.session.add(log)
        flash('Log added.')
        return redirect(url_for('.valve', tag=tag))
    logs = valve.logs.order_by(Log.date.desc())
    return render_template('valve.html', form=form, valve=valve, logs=logs)


@main.route('/valve/<int:id>/delete', methods=['POST'])
def valve_delete(id):
    valve = Valve.query.get_or_404(id)
    db.session.delete(valve)
    db.session.commit()
    flash('Valve deleted.')
    return redirect(url_for('.index'))


@main.route('/valve/<tag>/log/<int:log_id>/delete', methods=['POST'])
def log_delete(tag, log_id):
    log = Log.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    flash('Log deleted.')
    return redirect(url_for('.valve', tag=tag))

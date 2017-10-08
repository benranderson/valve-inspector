from flask import request, render_template, url_for, redirect, Response

from app.main import main
from app.main.forms import ValveForm
from app import db
from app.models import Valve


@main.route('/', methods=['GET', 'POST'])
def index():
    form = ValveForm()
    if form.validate_on_submit():
        valve = Valve(tag=form.tag.data, size=form.size.data)
        db.session.add(valve)
        return redirect(url_for('.index'))
    valves = Valve.query.all()
    return render_template('index.html', form=form, valves=valves)


@main.route('/valve/<tag>')
def valve(tag):
    valve = Valve.query.filter_by(tag=tag).first()
    return render_template('valve.html', valve=valve)

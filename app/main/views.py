from flask import request, render_template, url_for, redirect, Response, flash
from app.main import main
from app.main.forms import ProjectForm, ValveForm, LogForm
from app import db
from app.models import Project, Valve, Log
from flask_admin.menu import MenuLink


@main.route('/', methods=['GET', 'POST'])
def index():
    projects = Project.query.all()
    valves = Valve.query.all()
    return render_template('index.html', projects=projects, valves=valves)


@main.route('/valve/add', methods=['GET', 'POST'])
def valve_add():
    form = ValveForm()
    if form.validate_on_submit():
        valve = Valve(tag=form.tag.data, size=form.size.data,
                      location=form.location.data)
        db.session.add(valve)
        flash('Valve added.')
        return redirect(url_for('.index'))
    heading = "Add a new Valve"
    return render_template('edit.html', form=form, heading=heading)


@main.route('/project/add', methods=['GET', 'POST'])
def project_add():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(number=form.number.data,
                          title=form.title.data,
                          client=form.client.data,
                          vessel=form.vessel.data,
                          campaign=form.campaign.data,
                          date=form.date.data)
        db.session.add(project)
        flash('Project added.')
        return redirect(url_for('.index'))
    heading = "Add a new Project"
    return render_template('edit.html', form=form, heading=heading)


@main.route('/project/<int:id>', methods=['GET', 'POST'])
def project(id):
    project = Project.query.get_or_404(id)
    return render_template('project.html', project=project)


@main.route('/project/<int:id>/edit', methods=['GET', 'POST'])
def project_edit(id):
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.number = form.number.data
        project.title = form.title.data
        project.client = form.client.data
        project.vessel = form.vessel.data
        project.campaign = form.campaign.data
        project.date = form.date.data
        db.session.add(project)
        flash('Project updated.')
        return redirect(url_for('.index'))
    heading = "Edit Project"
    return render_template('edit.html', form=form, heading=heading)


@main.route('/project/<int:id>/delete', methods=['GET', 'POST'])
def project_delete(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted.')
    return redirect(url_for('.index'))


@main.route('/valve/<int:id>', methods=['GET', 'POST'])
def valve(id):
    valve = Valve.query.get_or_404(id)
    # latest_log = Log.query.filter_by(
    #     valve=valve).order_by(Log.date.desc()).first()
    form = LogForm()
    # form.status.default = latest_log.status
    # form.turns.default = latest_log.turns
    # form.process()
    if form.validate_on_submit():
        log = Log(date=form.date.data, status=form.status.data,
                  turns=form.turns.data)
        log.valve = valve
        db.session.add(log)
        db.session.commit()
        flash('Log added.')
        return redirect(url_for('.valve', id=id))
    logs = valve.logs.order_by(Log.date.desc())
    return render_template('valve.html', form=form, valve=valve, logs=logs)


@main.route('/valve/<int:id>/edit', methods=['GET', 'POST'])
def valve_edit(id):
    valve = Valve.query.get_or_404(id)
    form = ValveForm(obj=valve)
    if form.validate_on_submit():
        valve.tag = form.tag.data
        valve.size = form.size.data
        valve.location = form.location.data
        db.session.add(valve)
        db.session.commit()
        flash('Valve updated.')
        return redirect(url_for('.index'))
    heading = "Edit Valve"
    return render_template('edit.html', form=form, heading=heading)


@main.route('/valve/<int:id>/delete', methods=['GET', 'POST'])
def valve_delete(id):
    valve = Valve.query.get_or_404(id)
    db.session.delete(valve)
    db.session.commit()
    flash('Valve deleted.')
    return redirect(url_for('.index'))


@main.route('/valve/<int:valve_id>/log/<int:log_id>/edit', methods=['GET', 'POST'])
def log_edit(valve_id, log_id):
    log = Log.query.get_or_404(log_id)
    form = LogForm(obj=log)
    if form.validate_on_submit():
        log.date = form.date.data
        log.status = form.status.data
        log.turns = form.turns.data
        db.session.add(log)
        db.session.commit()
        flash('Log updated.')
        return redirect(url_for('.valve', id=valve_id))
    valve = Valve.query.get_or_404(valve_id)
    logs = valve.logs.order_by(Log.date.desc())
    return render_template('valve.html', form=form, valve=valve, logs=logs)


@main.route('/valve/<int:valve_id>/log/<int:log_id>/delete', methods=['GET', 'POST'])
def log_delete(valve_id, log_id):
    log = Log.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    flash('Log deleted.')
    return redirect(url_for('.valve', id=valve_id))

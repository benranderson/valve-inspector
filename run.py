#!/usr/bin/env python
import os
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import Valve, User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Valve=Valve)


@app.cli.command()
def test(cov=False):
    """Run the unit tests."""
    import pytest
    if cov:
        pytest.main(['--cov-report', 'term', '--cov-report',
                     'html:tmp/cov/', '--cov=app', TEST_PATH])
    else:
        pytest.main([TEST_PATH])


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()


@app.cli.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.
    """
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                print('Removing {}'.format(full_pathname))
                os.remove(full_pathname)

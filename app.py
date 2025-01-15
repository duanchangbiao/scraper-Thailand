from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app

from web import create_app
from web.extensions import db

from web.models.BaseModel import BaseModel
from web.models.models import SysJob
from web.route import scheduler

app = create_app()
with app.app_context():
    db.create_all()


def load_jobs():
    from web.view.job import add_job
    with app.app_context():
        jobs = SysJob.query.filter_by(status='0').all()
        for job in jobs:
            print(job.to_json())
            add_job(job.to_json())


@db.event.listens_for(BaseModel, 'before_update', propagate=True)
def execute_before_update(mapper, connection, target):
    with app.test_request_context():
        current_app.preprocess_request()
        target.before_update(mapper, connection, target)


@db.event.listens_for(BaseModel, 'before_insert', propagate=True)
def execute_before_insert(mapper, connection, target):
    with app.test_request_context():
        current_app.preprocess_request()
        target.before_insert(mapper, connection, target)


if __name__ == '__main__':
    load_jobs()
    scheduler.start()
    app.run(debug=True)

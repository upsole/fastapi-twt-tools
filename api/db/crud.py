from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
import os

import api.db.models as models
from twt_tools.lib.domain import Observer

DATABASE_URL = str(os.environ.get("DATABASE_URL"))

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind = engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def _reset_db():
    models.Base.metadata.create_all(engine)

def insert_job(session, file_format, filename=None):
    job = models.Job(status="pending", file=filename, format=file_format)
    session.add(job)
    session.commit()
    # return {col.name: getattr(job, col.name) for col in job.__table__.columns}
    return job.dict()

def query_job(session, job_id):
    job = session.query(models.Job).filter(models.Job.id == job_id).first()
    return job.dict()


def update_job(session, job_id, status="success", file=None):
    session.query(models.Job).filter(models.Job.id == job_id).update({"status": status, "file": file})
    session.commit()

def delete_job(session, job_id):
    session.query(models.Job).filter(models.Job.id == job_id).delete()
    session.commit()

class UserObserver(Observer):
    def __init__(self, job_id):
        self.job_id = job_id

    # BUG ???? whats going on here - update is being called with an extra argument (maybe job_id initialization messes it up?)
    def percent(_, state):
        return (state[0] / state[1]) * 100

    def update(self, _, user):
        if user._state:
            with session_scope() as s:
                s.query(models.Job).filter(models.Job.id == self.job_id).update({"progress": self.percent(user._state)})
                s.commit()

class ThreadObserver(Observer):
    def __init__(self, job_id):
        self.job_id = job_id

    # BUG ???? whats going on here - update is being called with an extra argument (maybe job_id initialization messes it up?)
    def percent(_, state):
        return (state[0] / state[1]) * 100

    def update(self, _, thread):
        if thread._state:
            with session_scope() as s:
                s.query(models.Job).filter(models.Job.id == self.job_id).update({"progress": self.percent(thread._state)})
                s.commit()

if __name__ == "__main__":
    _reset_db()
    print("Migrations done.")


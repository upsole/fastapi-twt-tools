from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
import os

import api.db.models as models

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

if __name__ == "__main__":
    _reset_db()
    print("Migrations done.")


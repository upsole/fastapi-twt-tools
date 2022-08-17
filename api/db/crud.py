import os
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

import models

# DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/twt_db"

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
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)

def _populate(session):
    for i in range(10):
        job = models.Job(status="success", file="pog.pdf")
        session.add(job)
    session.commit()
    print("Table job populated")


if __name__ == "__main__":
    _reset_db()
    with session_scope() as s:
        _populate(s)
    print("DB Reset")

    # with session_scope() as s:
    #     populate(s)
    # print("Table reseted")
    # pass

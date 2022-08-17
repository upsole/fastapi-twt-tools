from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer
# from sqlalchemy.dialects.postgresql

Base = declarative_base()

class Job(Base):
    __tablename__ = "job"

    # TODO use uuid
    id = Column(Integer, primary_key=True)
    # TODO must be enum of "inprogress" "failed" "success"
    status = Column(String)
    file = Column(String)

    # TODO expiresAt (?)
    # TODO createdAt (?)

    def __repr__(self):
        return f"<Job #{self.id} - Status: {self.status}>"

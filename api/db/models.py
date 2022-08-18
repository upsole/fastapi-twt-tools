from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Job(Base):
    __tablename__ = "job"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # TODO must be enum of "inprogress" "failed" "success"
    status = Column(String)
    file = Column(String)

    # TODO expiresAt (?)
    # TODO createdAt (?)

    def __repr__(self):
        return f"<Job #{self.id} - Status: {self.status}>"
    def dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

from sqlalchemy import Column, String, Text, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100))  # sql, python, spark, system_design, behavioral
    difficulty = Column(String(50))  # easy, medium, hard
    question_type = Column(String(50))  # coding, design, behavioral
    starter_code = Column(Text)
    test_cases = Column(JSONB)
    companies = Column(ARRAY(Text))  # Array of company names
    tags = Column(ARRAY(Text))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    attempts = relationship("Attempt", back_populates="question")

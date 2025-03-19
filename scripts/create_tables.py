from app.models.base import db

from app.models.user import User, Role, UserRole
from app.models.course import Course, StudentCourse
from app.models.assignment import Assignment, StudentAssignment
from app.models.learning_data import LearningActivity, KnowledgePoint, StudentKnowledgePoint
from app.models.knowledge_base import KnowledgeBase

from app import create_app

app = create_app()

tables = [
            User, Role, UserRole,
            Course, StudentCourse,
            Assignment, StudentAssignment,
            LearningActivity, KnowledgePoint, StudentKnowledgePoint,
            KnowledgeBase
        ]

db.drop_tables(tables)
db.create_tables(tables)
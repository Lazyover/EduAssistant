from peewee import *
from app.models.base import BaseModel
from app.models.course import Course
from app.models.user import User

class Assignment(BaseModel):
    title = CharField(max_length=100)
    description = TextField()
    course = ForeignKeyField(Course, backref='assignments')
    due_date = DateTimeField()
    total_points = FloatField(default=100.0)
    
    def __repr__(self):
        return f'<Assignment {self.title} for {self.course.code}>'

class StudentAssignment(BaseModel):
    student = ForeignKeyField(User, backref='assignments')
    assignment = ForeignKeyField(Assignment, backref='submissions')
    answer = TextField(null=True)
    feedback = TextField(null=True)
    score = FloatField(null=True)
    submitted_at = DateTimeField(null=True)
    attempts = IntegerField(default=0)
    completed = BooleanField(default=False)
    
    class Meta:
        indexes = (
            (('student', 'assignment'), True),  # 确保学生-作业组合唯一
        )

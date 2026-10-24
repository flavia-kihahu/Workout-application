from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()
class Exercise(db.Model):
    __tablename__ = "exercises"
    __table_args__ = (
        db.UniqueConstraint('name', name='uq_exercise_name'),
        db.CheckConstraint('length(trim(name)) > 0', name='ck_exercise_name_not_blank'),
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)
    workout_exercises = db.relationship("WorkoutExercises", back_populates="exercise", cascade='all, delete-orphan')
    workouts = association_proxy('workout_exercises', 'workout')
    @validates('name', 'category')
    def validate_text(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'{key} must be a non-empty string')
        return value.strip()
class Workout(db.Model):
    __tablename__ = "workouts"
    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='ck_workout_duration_positive'),
    )
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    workout_exercises = db.relationship("WorkoutExercises", back_populates="workout", cascade='all, delete-orphan')
    exercises = association_proxy('workout_exercises', 'exercise')
    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f'{key} must be a positive integer')
        return value
class WorkoutExercises(db.Model):
    __tablename__='workout_exercises'
    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='uq_workout_exercise_pair'),
        db.CheckConstraint('reps > 0', name='ck_workout_exercise_reps_positive'),
    )
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer)
    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")
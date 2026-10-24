from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from models import db, Workout, Exercise, WorkoutExercises
from schema import (
    workout_schema, workouts_schema,
    exercise_schema, exercises_schema,
    workout_exercise_schema
)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)
@app.get("/workouts")
def get_workouts():
    return jsonify(workouts_schema.dump(Workout.query.all()))
@app.get("/workouts/<int:id>")
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return {"error": "Workout not found"}, 404
    data = workout_schema.dump(workout)
    data["exercises"] = [{
        "exercise": exercise_schema.dump(link.exercise),
        "reps": link.reps, "sets": link.sets,
        "duration_seconds": link.duration_seconds
    } for link in workout.workout_exercises]
    return jsonify(data)
@app.post("/workouts")
def create_workout():
    try:
        workout = Workout(**workout_schema.load(request.get_json() or {}))
        db.session.add(workout)
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 201
    except (ValidationError, ValueError, TypeError) as error:
        db.session.rollback()
        return {"error": str(error)}, 400
@app.delete("/workouts/<int:id>")
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return {"error": "Workout not found"}, 404
    db.session.delete(workout)
    db.session.commit()
    return "", 204
@app.get("/exercises")
def get_exercises():
    return jsonify(exercises_schema.dump(Exercise.query.all()))
@app.get("/exercises/<int:id>")
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return {"error": "Exercise not found"}, 404
    data = exercise_schema.dump(exercise)
    data["workouts"] = [{
        "workout": workout_schema.dump(link.workout),
        "reps": link.reps, "sets": link.sets,
        "duration_seconds": link.duration_seconds
    } for link in exercise.workout_exercises]
    return jsonify(data)
@app.post("/exercises")
def create_exercise():
    try:
        exercise = Exercise(**exercise_schema.load(request.get_json() or {}))
        db.session.add(exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(exercise)), 201
    except (ValidationError, ValueError, TypeError) as error:
        db.session.rollback()
        return {"error": str(error)}, 400
@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return {"error": "Exercise not found"}, 404
    db.session.delete(exercise)
    db.session.commit()
    return "", 204
@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def add_exercise(workout_id, exercise_id):
    if not db.session.get(Workout, workout_id) or not db.session.get(Exercise, exercise_id):
        return {"error": "Workout or exercise not found"}, 404
    try:
        link = WorkoutExercises(
            workout_id=workout_id, exercise_id=exercise_id,
            **workout_exercise_schema.load(request.get_json() or {})
        )
        db.session.add(link)
        db.session.commit()
        return jsonify(workout_exercise_schema.dump(link)), 201
    except (ValidationError, ValueError, TypeError) as error:
        db.session.rollback()
        return {"error": str(error)}, 400
if __name__ == "__main__":
    app.run(port=5555, debug=True)
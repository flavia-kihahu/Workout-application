from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Workout, Exercise, WorkoutExercises

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)
@app.get("/workouts")
def get_workouts():
    return jsonify([{"id": w.id, "date": str(w.date),
                     "duration_minutes": w.duration_minutes, "notes": w.notes}
                    for w in Workout.query.all()])
@app.get("/workouts/<int:id>")
def get_workout(id):
    w = db.session.get(Workout, id)
    if not w:
        return {"error": "Workout not found"}, 404
    return jsonify({"id": w.id, "date": str(w.date),
                    "duration_minutes": w.duration_minutes, "notes": w.notes,
                    "exercises": [{"id": x.exercise.id, "name": x.exercise.name,
                                   "reps": x.reps, "sets": x.sets,
                                   "duration_seconds": x.duration_seconds}
                                  for x in w.workout_exercises]})
@app.post("/workouts")
def create_workout():
    data = request.json or {}
    w = Workout(date=__import__("datetime").date.fromisoformat(data["date"]),
                duration_minutes=data["duration_minutes"], notes=data.get("notes"))
    db.session.add(w)
    db.session.commit()
    return jsonify({"id": w.id, "date": str(w.date)}), 201
@app.delete("/workouts/<int:id>")
def delete_workout(id):
    w = db.session.get(Workout, id)
    if not w:
        return {"error": "Workout not found"}, 404
    db.session.delete(w)
    db.session.commit()
    return "", 204
@app.get("/exercises")
def get_exercises():
    return jsonify([{"id": e.id, "name": e.name, "category": e.category,
                     "equipment_needed": e.equipment_needed}
                    for e in Exercise.query.all()])

@app.get("/exercises/<int:id>")
def get_exercise(id):
    e = db.session.get(Exercise, id)
    if not e:
        return {"error": "Exercise not found"}, 404
    return jsonify({"id": e.id, "name": e.name, "category": e.category,
                    "equipment_needed": e.equipment_needed,
                    "workouts": [{"id": x.workout.id, "reps": x.reps,
                                  "sets": x.sets, "duration_seconds": x.duration_seconds}
                                 for x in e.workout_exercises]})
@app.post("/exercises")
def create_exercise():
    data = request.json or {}
    e = Exercise(name=data["name"], category=data["category"],
                 equipment_needed=data.get("equipment_needed", False))
    db.session.add(e)
    db.session.commit()
    return jsonify({"id": e.id, "name": e.name}), 201
@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    e = db.session.get(Exercise, id)
    if not e:
        return {"error": "Exercise not found"}, 404
    db.session.delete(e)
    db.session.commit()
    return "", 204
@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def add_exercise(workout_id, exercise_id):
    if not db.session.get(Workout, workout_id) or not db.session.get(Exercise, exercise_id):
        return {"error": "Workout or exercise not found"}, 404
    x = WorkoutExercises(workout_id=workout_id, exercise_id=exercise_id,
                         **{k: (request.json or {}).get(k)
                            for k in ("reps", "sets", "duration_seconds")})
    db.session.add(x)
    db.session.commit()
    return jsonify({"id": x.id, "workout_id": workout_id,
                    "exercise_id": exercise_id}), 201
if __name__ == "__main__":
    app.run(port=5555, debug=True)
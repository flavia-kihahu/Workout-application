from app import app
from models import db, Exercise, Workout, WorkoutExercises
from datetime import date

with app.app_context():
    print("Clearing tables...")
    WorkoutExercises.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()
    print("Seeding exercises...")

    squat = Exercise(
        name="Squat",
        category="Strength",
        equipment_needed=True,
    )
    pushup = Exercise(
        name="Push-up",
        category="Strength",
        equipment_needed=False,
    )
    plank = Exercise(
        name="Plank",
        category="Core",
        equipment_needed=False,
    )
    run = Exercise(
        name="Treadmill Run",
        category="Cardio",
        equipment_needed=True,
    )

    db.session.add_all([squat, pushup, plank, run])
    print("Seeding workouts...")
    w1 = Workout(
        date=date(2026, 10, 19),
        duration_minutes=45,
        notes="Lower body focus",
    )
    w2 = Workout(
        date=date(2026, 10, 21),
        duration_minutes=30,
        notes="Quick full-body session",
    )
    w3 = Workout(
        date=date(2026, 10, 22),
        duration_minutes=60,
    )
    db.session.add_all([w1, w2, w3])
    db.session.commit()
    print("Linking exercises to workouts...")
    db.session.add_all([
        WorkoutExercises(
            workout=w1, exercise=squat, reps=10, sets=4
        ),
        WorkoutExercises(
            workout=w1, exercise=plank,
            duration_seconds=60, sets=3
        ),
        WorkoutExercises(
            workout=w2, exercise=pushup, reps=15, sets=3
        ),
        WorkoutExercises(
            workout=w2, exercise=plank,
            duration_seconds=45, sets=2
        ),
        WorkoutExercises(
            workout=w3, exercise=run,
            duration_seconds=1200
        ),
        WorkoutExercises(
            workout=w3, exercise=squat, reps=8, sets=5
        ),
    ])
    db.session.commit()
    print("Done!")
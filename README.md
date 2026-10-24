# Workout Tracker API

A RESTful API built with Flask, SQLAlchemy, and Marshmallow for managing workouts and exercises. It supports creating, retrieving, and deleting workouts and exercises, associating exercises with workouts, and validating data to maintain database integrity.

## Technologies
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLAlchemy
- Marshmallow
- SQLite

## Setup and Installation

### Prerequisites

- Python
- Pipenv

### Installation

From the project root, run:
pipenv install
pipenv shell
cd server

### Database Setup

If migrations have not been initialized yet, run:
flask db init
Then apply migrations:
flask db migrate -m "create workout tables"
flask db upgrade

If the `migrations` directory already exists, skip `flask db init`.
### Seed the Database
python seed.py

### Run the Application
python app.py

The API runs at `http://127.0.0.1:5555`.

## API Endpoints
| Method | Path | Purpose |
|---|---|---|
| GET | /workouts | List all workouts |
| GET | /workouts/<id> | Retrieve a workout and its exercises |
| POST | /workouts | Create a workout |
| DELETE |/workouts/<id> | Delete a workout |
| GET | /exercises | List all exercises |
| GET | /exercises/<id> | Retrieve an exercise and its workout associations |
| POST | /exercises | Create an exercise |
| DELETE | /exercises/<id> | Delete an exercise |
| POST | /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises | Add an exercise to a workout |

## Validation and Data Integrity
The application uses database constraints, model validations, and Marshmallow schema validations to help ensure valid data.

- **Table constraints:** Unique exercise names, non-blank names and categories, positive workout durations, non-negative exercise metrics, and unique workout-exercise pairs.
- **Model validations:** Validate exercise names and categories, equipment requirements, workout duration, notes, and exercise metrics.
- **Schema validations:** Validate input fields, date formats, numeric ranges, strict integer values, and exercise activity requirements.

## Testing

API endpoints can be tested using Postman. Use the base URL:
http://127.0.0.1:5555

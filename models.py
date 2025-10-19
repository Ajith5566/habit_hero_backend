from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Habit(db.Model):
    # Primary key id for habit record
    id = db.Column(db.Integer, primary_key=True)

    # Name of the habit, required (cannot be null)
    name = db.Column(db.String(100), nullable=False)

    # Frequency string like daily, weekly — required
    frequency = db.Column(db.String(50), nullable=False)

    # Category of habit like health, work — required
    category = db.Column(db.String(50), nullable=False)

    # Start date of the habit in string format (e.g. 'YYYY-MM-DD') — required
    start_date = db.Column(db.String(50), nullable=False)

    # Integer progress counter, defaults to 0
    progress = db.Column(db.Integer, default=0)

    # Define one-to-many relationship to Checkin model
    # 'backref' allows accessing habit from checkin via 'habit' attribute
    # 'lazy=True' means checkins are loaded on-demand
    # 'cascade="all, delete-orphan"' deletes related checkins when habit deleted
    checkins = db.relationship(
        'Checkin',
        backref='habit',
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Convert Habit model instance to a dictionary for JSON serializing
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "frequency": self.frequency,
            "category": self.category,
            "start_date": self.start_date,
            "progress": self.progress,
            # Number of associated checkins (habit completions)
            "checkin_count": len(self.checkins),
            # List of dates for all checkins linked to this habit
            "checkin_dates": [c.date for c in self.checkins],
        }

class Checkin(db.Model):
    # Primary key for checkin record
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key to parent habit's id; required field
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)

    # Date string representing the check-in date (format 'YYYY-MM-DD')
    date = db.Column(db.String(50), nullable=False)

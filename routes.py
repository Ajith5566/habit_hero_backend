from flask import Blueprint, request, jsonify
from models import db, Habit, Checkin
from datetime import datetime, timedelta
from collections import Counter

habit_routes = Blueprint('habit_routes', __name__)

# GET /habits - Return list of all habits in JSON format
@habit_routes.route('/habits', methods=['GET'])
def get_habits():
    habits = Habit.query.all()
    return jsonify([h.to_dict() for h in habits])

# POST /habits - Create a new habit with posted JSON data
@habit_routes.route('/habits', methods=['POST'])
def add_habit():
    data = request.json
    new_habit = Habit(
        name=data['name'],
        frequency=data['frequency'],
        category=data['category'],
        start_date=data['start_date'],
        progress=0
    )
    db.session.add(new_habit)
    db.session.commit()
    return jsonify(new_habit.to_dict()), 201

# PUT /habits/<id> - Update habit by ID with provided JSON data
@habit_routes.route('/habits/<int:id>', methods=['PUT'])
def update_habit(id):
    habit = Habit.query.get_or_404(id)
    data = request.json
    habit.name = data.get('name', habit.name)
    habit.frequency = data.get('frequency', habit.frequency)
    habit.category = data.get('category', habit.category)
    habit.start_date = data.get('start_date', habit.start_date)
    habit.progress = data.get('progress', habit.progress)
    db.session.commit()
    return jsonify(habit.to_dict())

# DELETE /habits/<id> - Remove habit by ID and all associated checkins
@habit_routes.route('/habits/<int:id>', methods=['DELETE'])
def delete_habit(id):
    habit = Habit.query.get_or_404(id)
    db.session.delete(habit)
    db.session.commit()
    return '', 204

# POST /habits/<habit_id>/checkins - Add a check-in for today if not already checked in
@habit_routes.route('/habits/<int:habit_id>/checkins', methods=['POST'])
def add_checkin(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    today = datetime.today().strftime('%Y-%m-%d')
    # Prevent duplicate check-ins for the same day
    if any(c.date == today for c in habit.checkins):
        return {"message": "Already checked in today"}, 400
    new_checkin = Checkin(habit_id=habit_id, date=today)
    db.session.add(new_checkin)
    db.session.commit()
    return {"message": "Check-in successful"}

# GET /habits/<habit_id>/checkins - Get all check-in dates for a habit
@habit_routes.route('/habits/<int:habit_id>/checkins', methods=['GET'])
def get_checkins(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    return jsonify([c.date for c in habit.checkins])

# GET /analytics - Compute and return aggregated analytics data
@habit_routes.route('/analytics', methods=['GET'])
def get_analytics():
    habits = Habit.query.all()
    total_habits = len(habits)
    total_progress = sum(len(h.checkins) for h in habits)

    # Helper function calculates current streak of consecutive daily check-ins
    def habit_streak(habit):
        dates = sorted([datetime.strptime(c.date, '%Y-%m-%d') for c in habit.checkins], reverse=True)
        streak = 0
        today = datetime.today()
        for i, date in enumerate(dates):
            expected_date = today - timedelta(days=i)
            if date.date() == expected_date.date():
                streak += 1
            else:
                break
        return streak

    success_rates = []
    streaks = []
    for h in habits:
        start = datetime.strptime(h.start_date, '%Y-%m-%d')
        delta_days = (datetime.today() - start).days + 1
        checked_days = len(h.checkins)
        # Calculate success rate = check-ins divided by days active
        rate = checked_days / delta_days if delta_days > 0 else 0
        success_rates.append(rate)
        streaks.append(habit_streak(h))

    average_success_rate = sum(success_rates) / total_habits if total_habits > 0 else 0
    best_streak = max(streaks) if streaks else 0

    # Aggregate dates from all check-ins across habits
    all_checkin_dates = []
    for h in habits:
        all_checkin_dates.extend([c.date for c in h.checkins])
    # Count which weekday is most common among check-in dates
    weekdays = [datetime.strptime(d, '%Y-%m-%d').strftime('%A') for d in all_checkin_dates]
    most_common_day = Counter(weekdays).most_common(1)[0][0] if weekdays else None

    # Return analytics summary JSON
    return jsonify({
        "total_habits": total_habits,
        "total_progress": total_progress,
        "average_success_rate": average_success_rate,
        "best_streak": best_streak,
        "best_day": most_common_day
    })

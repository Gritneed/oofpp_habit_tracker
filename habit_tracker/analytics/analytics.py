
from datetime import datetime, timedelta

def get_completion_rate(check_dates, periodicity, start_date):
    """Calculate habit completion rate."""
    if not check_dates:
        return 0.0
    
    # Ensure all dates are datetime objects
    check_dates = [d if isinstance(d, datetime) else datetime.combine(d, datetime.min.time()) 
                  for d in check_dates]
    start_date = start_date if isinstance(start_date, datetime) else datetime.combine(start_date, datetime.min.time())
    
    # Calculate the number of days in the period
    days_in_period = (datetime.now() - start_date).days + 1
    completed_days = len(set(d.date() for d in check_dates))
    
    return (completed_days / days_in_period) * 100
def get_habit_patterns(check_dates):
    """Analyze habit completion patterns by time of day."""
    patterns = {
        'morning': 0,    # 6-12
        'afternoon': 0,  # 12-18
        'evening': 0,    # 18-24
        'night': 0       # 0-6
    }
    
    for date in check_dates:
        hour = date.hour
        if 6 <= hour < 12:
            patterns['morning'] += 1
        elif 12 <= hour < 18:
            patterns['afternoon'] += 1
        elif 18 <= hour < 24:
            patterns['evening'] += 1
        else:
            patterns['night'] += 1
            
    return patterns

def analyze_habit_trends(habits):
    """Analyze overall habit trends."""
    if not habits:
        return {
            'total_habits': 0,
            'most_successful': None,
            'least_successful': None,
            'by_periodicity': {}
        }
    
    # Find most and least successful habits
    sorted_habits = sorted(habits, key=lambda x: x['completion_rate'], reverse=True)
    
    # Group habits by periodicity
    by_periodicity = {}
    for habit in habits:
        period = habit['periodicity']
        if period not in by_periodicity:
            by_periodicity[period] = 0
        by_periodicity[period] += 1
    
    return {
        'total_habits': len(habits),
        'most_successful': sorted_habits[0]['name'],
        'least_successful': sorted_habits[-1]['name'],
        'by_periodicity': by_periodicity
    }

def get_streak_analysis(check_dates, periodicity):
    """Analyze streaks in habit completion."""
    if not check_dates:
        return {'current_streak': 0, 'longest_streak': 0}
    
    # Convert all dates to datetime if they aren't already
    dates = [d if isinstance(d, datetime) else datetime.combine(d, datetime.min.time()) 
            for d in check_dates]
    
    # Sort dates in reverse chronological order (newest first)
    dates = sorted(dates, reverse=True)
    
    current_streak = 1
    longest_streak = 1
    today = datetime.now().date()
    
    # Check if the most recent completion was today or yesterday
    if not (dates[0].date() == today or dates[0].date() == today - timedelta(days=1)):
        current_streak = 0
    else:
        for i in range(len(dates) - 1):
            current_date = dates[i].date()
            next_date = dates[i + 1].date()
            
            if (current_date - next_date).days == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                if i == 0:  # If break is at the start, reset current streak
                    current_streak = 1
                break
    
    return {
        'current_streak': current_streak,
        'longest_streak': longest_streak
    }
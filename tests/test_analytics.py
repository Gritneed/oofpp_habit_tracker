from datetime import datetime, timedelta
from habit_tracker.analytics.analytics import (
    get_completion_rate,
    get_streak_analysis,
    get_habit_patterns,
    analyze_habit_trends
)

def test_completion_rate():
    """Test habit completion rate calculation."""
    # Set fixed dates for consistent testing
    today = datetime.now()
    start_date = today - timedelta(days=10)
    check_dates = [
        today - timedelta(days=i)
        for i in [1, 2, 3, 5, 7]
    ]
    
    rate = get_completion_rate(check_dates, "daily", start_date)
    assert 0 <= rate <= 100
    expected_rate = (5 / 11) * 100
    assert abs(rate - expected_rate) < 0.01  # Allow for small floating-point differences

def test_habit_patterns():
    """Test habit pattern analysis."""
    check_dates = [
        datetime(2024, 1, 1, 8, 0),  # morning
        datetime(2024, 1, 2, 13, 0),  # afternoon
        datetime(2024, 1, 3, 20, 0),  # evening
    ]
    
    patterns = get_habit_patterns(check_dates)
    assert patterns['morning'] == 1
    assert patterns['afternoon'] == 1
    assert patterns['evening'] == 1
    assert patterns['night'] == 0

def test_streak_analysis():
    """Test streak calculation."""
    today = datetime.now()
    check_dates = [
        today - timedelta(days=i)
        for i in range(5)  # Last 5 consecutive days
    ]
    
    analysis = get_streak_analysis(check_dates, "daily")
    assert analysis['current_streak'] == 5
    assert analysis['longest_streak'] == 5  # Changed from 'max_streak' to 'longest_streak'

def test_habit_trends():
    """Test overall habit trend analysis."""
    habits = [
        {
            'name': 'Habit 1',
            'periodicity': 'daily',
            'completion_rate': 80.0
        },
        {
            'name': 'Habit 2',
            'periodicity': 'daily',
            'completion_rate': 60.0
        }
    ]
    
    trends = analyze_habit_trends(habits)
    assert trends['total_habits'] == 2
    assert trends['most_successful'] == 'Habit 1'
    assert trends['least_successful'] == 'Habit 2'
    assert 'daily' in trends['by_periodicity']
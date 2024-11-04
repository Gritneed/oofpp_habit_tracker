import pytest
from datetime import datetime, timedelta
from habit_tracker.models.habit import Habit

def test_habit_creation():
    """Test basic habit creation."""
    habit = Habit(1, "Test Habit", "daily")
    assert habit.name == "Test Habit"
    assert habit.periodicity == "daily"
    assert habit.streak_count == 0
    assert habit.total_check_count == 0

def test_invalid_periodicity():
    """Test that invalid periodicity raises error."""
    with pytest.raises(ValueError):
        Habit(1, "Test Habit", "monthly")

def test_habit_check_off(sample_habit):
    """Test habit completion."""
    initial_count = sample_habit.total_check_count
    sample_habit.check_off()
    assert sample_habit.total_check_count == initial_count + 1
    assert sample_habit.last_check_date is not None

def test_habit_to_dict(sample_habit):
    """Test habit serialization."""
    habit_dict = sample_habit.to_dict()
    assert habit_dict['name'] == "Test Habit"
    assert habit_dict['periodicity'] == "daily"
    assert 'creation_date' in habit_dict

def test_habit_from_dict():
    """Test habit deserialization."""
    data = {
        'id': 1,
        'name': "Test Habit",
        'periodicity': "daily",
        'creation_date': datetime.now().isoformat(),
        'last_check_date': None,
        'is_active': True,
        'streak_count': 0,
        'total_check_count': 0
    }
    habit = Habit.from_dict(data)
    assert habit.name == "Test Habit"
    assert habit.periodicity == "daily"
from datetime import datetime, timedelta
from habit_tracker.utils.habit_validator import HabitValidator

def test_habit_creation_validation():
    """Test habit creation validation."""
    # Valid case
    is_valid, error = HabitValidator.validate_habit_creation(
        "Test Habit", "daily"
    )
    assert is_valid
    assert error is None
    
    # Invalid periodicity
    is_valid, error = HabitValidator.validate_habit_creation(
        "Test Habit", "monthly"
    )
    assert not is_valid
    assert "periodicity" in error.lower()
    
    # Empty name
    is_valid, error = HabitValidator.validate_habit_creation(
        "", "daily"
    )
    assert not is_valid
    assert "name" in error.lower()

def test_habit_completion_validation():
    """Test habit completion validation."""
    now = datetime.now()
    
    # First completion
    is_valid, error = HabitValidator.validate_habit_completion(
        None, "daily"
    )
    assert is_valid
    assert error is None
    
    # Same day completion
    is_valid, error = HabitValidator.validate_habit_completion(
        now, "daily"
    )
    assert not is_valid
    assert "already checked" in error.lower()
    
    # Different day completion
    is_valid, error = HabitValidator.validate_habit_completion(
        now - timedelta(days=1), "daily"
    )
    assert is_valid
    assert error is None
import pytest
from habit_tracker.models.habit_manager import HabitManager

def test_add_habit(habit_manager):
    """Test adding a new habit."""
    habit = habit_manager.add_habit("Test Habit", "daily")
    assert habit.name == "Test Habit"
    assert len(habit_manager.habits) == 1

def test_max_habits(habit_manager):
    """Test maximum habits limit."""
    for i in range(10):
        habit_manager.add_habit(f"Habit {i}", "daily")
    
    with pytest.raises(ValueError, match="Maximum number of habits"):
        habit_manager.add_habit("One Too Many", "daily")

def test_remove_habit(habit_manager):
    """Test removing a habit."""
    habit = habit_manager.add_habit("Test Habit", "daily")
    habit_id = habit.id
    assert len(habit_manager.habits) == 1
    
    habit_manager.remove_habit(habit_id)
    assert len(habit_manager.habits) == 0

def test_get_habits_by_periodicity(habit_manager):
    """Test filtering habits by periodicity."""
    habit_manager.add_habit("Daily Habit", "daily")
    habit_manager.add_habit("Weekly Habit", "weekly")
    
    daily_habits = habit_manager.get_habits_by_periodicity("daily")
    weekly_habits = habit_manager.get_habits_by_periodicity("weekly")
    
    assert len(daily_habits) == 1
    assert len(weekly_habits) == 1
    assert daily_habits[0].name == "Daily Habit"
    assert weekly_habits[0].name == "Weekly Habit"

def test_data_persistence(temp_db):
    """Test saving and loading habits."""
    # Create first manager and add habit
    manager1 = HabitManager(storage_path=temp_db)
    manager1.add_habit("Persistent Habit", "daily")
    
    # Create second manager to load data
    manager2 = HabitManager(storage_path=temp_db)
    assert len(manager2.habits) == 1
    assert manager2.habits[0].name == "Persistent Habit"
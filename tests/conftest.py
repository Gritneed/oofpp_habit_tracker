import pytest
from datetime import datetime, timedelta
import os
import json
import tempfile
from habit_tracker.models.habit import Habit
from habit_tracker.models.habit_manager import HabitManager
from pathlib import Path
import sys

@pytest.fixture
def temp_db():
    """Create a temporary JSON file for testing."""
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, 'test_habits.json')
    with open(temp_file, 'w') as f:
        json.dump([], f)
    yield temp_file
    os.remove(temp_file)
    os.rmdir(temp_dir)

@pytest.fixture
def sample_habit():
    """Create a sample habit for testing."""
    return Habit(
        id=1,
        name="Test Habit",
        periodicity="daily",
        creation_date=datetime.now()
    )

@pytest.fixture
def habit_manager(temp_db):
    """Create a HabitManager instance with temporary storage."""
    return HabitManager(storage_path=temp_db)
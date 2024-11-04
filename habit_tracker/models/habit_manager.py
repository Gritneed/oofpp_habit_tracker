import json
import os
from typing import List, Optional
from .habit import Habit

class HabitManager:
    """Manages the collection of habits."""
    
    def __init__(self, storage_path: str = 'data/habits_data.json'):
        """
        Initialize the habit manager.
        
        Args:
            storage_path: Path to the JSON file for storing habits
        """
        if storage_path is None:
            # Get the directory where habit_manager.py is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to the habit_tracker package directory
            package_dir = os.path.dirname(current_dir)
            # Construct path to data directory
            data_dir = os.path.join(package_dir, 'data')
            # Create data directory if it doesn't exist
            os.makedirs(data_dir, exist_ok=True)
            # Set the full path to the JSON file
            self.storage_path = os.path.join(data_dir, 'habits_data.json')
        else:
            self.storage_path = storage_path

        self.habits: List[Habit] = []
        self.load_data()
    
    def add_habit(self, name: str, periodicity: str) -> Habit:
        """
        Add a new habit to track.
        
        Args:
            name: Name of the habit
            periodicity: 'daily' or 'weekly'
            
        Returns:
            The newly created Habit instance
        """
        if len(self.habits) >= 10:
            raise ValueError("Maximum number of habits (10) reached")
        
        new_id = max([h.id for h in self.habits], default=0) + 1
        habit = Habit(id=new_id, name=name, periodicity=periodicity)
        self.habits.append(habit)
        self.save_data()
        return habit
    
    def remove_habit(self, habit_id: int) -> None:
        """
        Remove a habit from tracking.
        
        Args:
            habit_id: ID of the habit to remove
        """
        self.habits = [h for h in self.habits if h.id != habit_id]
        self.save_data()
    
    def get_habit_by_id(self, habit_id: int) -> Optional[Habit]:
        """Get a habit by its ID."""
        return next((h for h in self.habits if h.id == habit_id), None)
    
    def get_habits_by_periodicity(self, periodicity: str) -> List[Habit]:
        """Get all habits with the specified periodicity."""
        return [h for h in self.habits if h.periodicity == periodicity.lower()]
    
    def save_data(self) -> None:
        """Save habits to JSON file."""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        
        data = [habit.to_dict() for habit in self.habits]
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self) -> None:
        """Load habits from JSON file."""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                self.habits = [Habit.from_dict(item) for item in data]
        except FileNotFoundError:
            # Create empty file if it doesn't exist
            self.habits = []
            self.save_data()
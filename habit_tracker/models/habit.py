from datetime import datetime
from typing import Optional

class Habit:
    """A class representing a habit to be tracked."""
    
    def __init__(self, 
                 id: int,
                 name: str, 
                 periodicity: str,
                 creation_date: Optional[datetime] = None):
        """
        Initialize a new habit.
        
        Args:
            id: Unique identifier for the habit
            name: Name of the habit
            periodicity: 'daily' or 'weekly'
            creation_date: When the habit was created (defaults to now)
        """
        self.id = id
        self.name = name
        self.periodicity = periodicity.lower()
        self.creation_date = creation_date or datetime.now()
        self.last_check_date = None
        self.is_active = True
        self.streak_count = 0
        self.total_check_count = 0
        
        if self.periodicity not in ['daily', 'weekly']:
            raise ValueError("Periodicity must be 'daily' or 'weekly'")
    
    def check_off(self) -> None:
        """Mark the habit as completed for the current period."""
        self.last_check_date = datetime.now()
        self.total_check_count += 1
        self._update_streak()
    
    def _update_streak(self) -> None:
        """Update the streak count based on completion timing."""
        # This will be implemented with streak calculation logic
        pass
    
    def to_dict(self) -> dict:
        """Convert the habit to a dictionary for storage."""
        return {
            'id': self.id,
            'name': self.name,
            'periodicity': self.periodicity,
            'creation_date': self.creation_date.isoformat(),
            'last_check_date': self.last_check_date.isoformat() if self.last_check_date else None,
            'is_active': self.is_active,
            'streak_count': self.streak_count,
            'total_check_count': self.total_check_count
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Habit':
        """Create a Habit instance from a dictionary."""
        habit = cls(
            id=data['id'],
            name=data['name'],
            periodicity=data['periodicity'],
            creation_date=datetime.fromisoformat(data['creation_date'])
        )
        if data['last_check_date']:
            habit.last_check_date = datetime.fromisoformat(data['last_check_date'])
        habit.is_active = data['is_active']
        habit.streak_count = data['streak_count']
        habit.total_check_count = data['total_check_count']
        return habit
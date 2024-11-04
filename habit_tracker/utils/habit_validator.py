from datetime import datetime, timedelta
from typing import Optional

class HabitValidator:
    """Validates habit creation and completion."""
    
    @staticmethod
    def validate_habit_creation(name: str, periodicity: str) -> tuple[bool, Optional[str]]:
        """
        Validate habit creation parameters.
        
        Args:
            name: Name of the habit
            periodicity: Frequency of the habit ('daily' or 'weekly')
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name or len(name.strip()) == 0:
            return False, "Habit name cannot be empty"
            
        if len(name) > 100:
            return False, "Habit name cannot exceed 100 characters"
            
        if periodicity.lower() not in ['daily', 'weekly']:
            return False, "Periodicity must be either 'daily' or 'weekly'"
            
        return True, None

    @staticmethod
    def validate_habit_completion(last_check_date: Optional[datetime], periodicity: str) -> tuple[bool, Optional[str]]:
        """
        Validate if a habit can be checked off.
        
        Args:
            last_check_date: The last time the habit was checked off
            periodicity: Frequency of the habit ('daily' or 'weekly')
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not last_check_date:
            return True, None
            
        now = datetime.now()
        if periodicity == 'daily':
            if last_check_date.date() == now.date():
                return False, "Habit already checked off today"
        else:  # weekly
            week_start = now - timedelta(days=now.weekday())
            last_week_start = last_check_date - timedelta(days=last_check_date.weekday())
            if week_start == last_week_start:
                return False, "Habit already checked off this week"
                
        return True, None
from datetime import datetime, timedelta
from typing import List, Optional

class StreakCalculator:
    """Calculates streaks for habits."""
    
    @staticmethod
    def calculate_current_streak(check_dates: List[datetime], periodicity: str) -> int:
        """
        Calculate the current streak for a habit.
        
        Args:
            check_dates: List of completion dates
            periodicity: 'daily' or 'weekly'
            
        Returns:
            Current streak count
        """
        if not check_dates:
            return 0
            
        sorted_dates = sorted(check_dates, reverse=True)
        current_date = datetime.now()
        streak = 0
        
        for i, date in enumerate(sorted_dates):
            if periodicity == 'daily':
                expected_date = current_date - timedelta(days=i)
                if date.date() != expected_date.date():
                    break
            else:  # weekly
                week_diff = (current_date - date).days // 7
                if week_diff != i:
                    break
            streak += 1
            
        return streak

    @staticmethod
    def calculate_longest_streak(check_dates: List[datetime], periodicity: str) -> int:
        """
        Calculate the longest streak achieved.
        
        Args:
            check_dates: List of completion dates
            periodicity: 'daily' or 'weekly'
            
        Returns:
            Longest streak count
        """
        if not check_dates:
            return 0
            
        sorted_dates = sorted(check_dates)
        longest_streak = current_streak = 1
        
        for i in range(1, len(sorted_dates)):
            if periodicity == 'daily':
                expected_date = sorted_dates[i-1] + timedelta(days=1)
                if sorted_dates[i].date() == expected_date.date():
                    current_streak += 1
                else:
                    current_streak = 1
            else:  # weekly
                week_diff = (sorted_dates[i] - sorted_dates[i-1]).days // 7
                if week_diff == 1:
                    current_streak += 1
                else:
                    current_streak = 1
                    
            longest_streak = max(longest_streak, current_streak)
            
        return longest_streak
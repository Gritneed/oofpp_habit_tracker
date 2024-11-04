
import calendar
from datetime import datetime, timedelta
from typing import List, Dict

class CalendarView:
    """Displays habits in a monthly calendar format."""
    def __init__(self):
        self.current_date = datetime.now()
        self.calendar = calendar.TextCalendar(firstweekday=calendar.MONDAY)

    def display_month(self, habits, year, month):
        """Display calendar for a specific month with habit completions."""
        # Get the calendar for the specified month
        cal = self.calendar.formatmonth(year, month)
        
        # Add completion markers
        cal_lines = cal.split('\n')
        result_lines = [cal_lines[0], cal_lines[1]]  # Keep header and day names
        
        # Process each week
        for week in cal_lines[2:]:
            if week.strip():  # Skip empty lines
                week_line = ''
                for day in week.split():
                    if day.strip():
                        date = datetime(year, month, int(day))
                        marker = 'X' if self._get_completion_status(date, habits) else ' '
                        week_line += f'{day:2}{marker} '
                    else:
                        week_line += '    '  # Space for empty days
                result_lines.append(week_line.rstrip())
        
        return '\n'.join(result_lines)

    def next_month(self):
        """Navigate to next month."""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)

    def previous_month(self):
        """Navigate to previous month."""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)

    def _get_completion_status(self, date, habits):
        """Check if any habit was completed on the given date."""
        target_date = date.date()
        return any(
            hasattr(habit, 'completions') and  # Check if habit has completions attribute
            any(completion.date() == target_date 
                for completion in habit.completions)
            for habit in habits
        )
    
    @staticmethod
    def generate_monthly_view(habits: List['Habit'], year: int = None, month: int = None) -> str:
        """
        Generate a monthly calendar view showing habit completions.
        
        Args:
            habits: List of habits to display
            year: Year to display (defaults to current year)
            month: Month to display (defaults to current month)
        
        Returns:
            Formatted string showing the calendar
        """
        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month
            
        # Get the calendar for the specified month
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        
        # Create header
        output = [f"\n{month_name} {year}".center(50)]
        output.append("-" * 50)
        output.append("Mon  Tue  Wed  Thu  Fri  Sat  Sun")
        
        # Generate completion marks for each habit
        habit_marks = {}
        for habit in habits:
            if habit.last_check_date:
                date_key = habit.last_check_date.strftime("%Y-%m-%d")
                if date_key not in habit_marks:
                    habit_marks[date_key] = []
                habit_marks[date_key].append(habit.name[0])  # First letter of habit name
        
        # Generate calendar rows
        for week in cal:
            week_str = []
            for day in week:
                if day == 0:
                    week_str.append("    ")
                else:
                    date = datetime(year, month, day)
                    date_key = date.strftime("%Y-%m-%d")
                    if date_key in habit_marks:
                        marks = "".join(habit_marks[date_key])
                        day_str = f"{day:2d}{marks}"
                    else:
                        day_str = f"{day:2d} "
                    week_str.append(day_str.ljust(4))
            output.append("  ".join(week_str))
            
        return "\n".join(output)

    @staticmethod
    def get_habit_summary(habits: List['Habit']) -> str:
        """Generate a summary of habits and their markers."""
        if not habits:
            return "No habits defined"
            
        output = ["\nHabit markers:"]
        for habit in habits:
            output.append(f"{habit.name[0]}: {habit.name}")
        return "\n".join(output)
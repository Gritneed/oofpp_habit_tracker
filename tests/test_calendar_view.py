import pytest
from datetime import datetime
from habit_tracker.utils.calendar_view import CalendarView
from habit_tracker.models.habit import Habit

class TestCalendarView:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        self.calendar_view = CalendarView()
        
        # Sample test data
        self.test_habits = [
            Habit(
                id=1,
                name="Test Habit 1",
                periodicity="daily",
                creation_date=datetime(2024, 3, 1)
            )
        ]
        # Add some completions to the test habit
        self.test_habits[0].completions = [datetime(2024, 3, 1)]

    def test_display_month(self):
        """Test displaying a specific month."""
        calendar_output = self.calendar_view.display_month(self.test_habits, 2024, 3)
        assert isinstance(calendar_output, str)
        assert "2024" in calendar_output

    def test_completion_status(self):
        """Test completion status checking."""
        date_with_completion = datetime(2024, 3, 1)
        assert self.calendar_view._get_completion_status(date_with_completion, self.test_habits)
        
        date_without_completion = datetime(2024, 3, 2)
        assert not self.calendar_view._get_completion_status(date_without_completion, self.test_habits)

    def test_navigation(self):
        """Test month navigation."""
        self.calendar_view.current_date = datetime(2024, 3, 1)
        
        self.calendar_view.next_month()
        assert self.calendar_view.current_date.month == 4
        
        self.calendar_view.previous_month()
        assert self.calendar_view.current_date.month == 3
        
        self.calendar_view.previous_month()
        assert self.calendar_view.current_date.month == 2
        
        # Test previous month
        self.calendar_view.previous_month()
        assert self.calendar_view.current_date.month == 1
        
        # Test year transition forward
        self.calendar_view.current_date = datetime(2024, 12, 1)
        self.calendar_view.next_month()
        assert self.calendar_view.current_date.year == 2025
        assert self.calendar_view.current_date.month == 1
        
        # Test year transition backward
        self.calendar_view.current_date = datetime(2024, 1, 1)
        self.calendar_view.previous_month()
        assert self.calendar_view.current_date.year == 2023
        assert self.calendar_view.current_date.month == 12

if __name__ == '__main__':
    unittest.main()
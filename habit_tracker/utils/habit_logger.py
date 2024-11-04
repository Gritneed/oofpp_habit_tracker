import logging
import os
import json
from datetime import datetime
from pythonjsonlogger import jsonlogger

class HabitLogger:
    """Logs habit-related actions."""
    
    def __init__(self, log_file: str = None):
        """Initialize the logger."""
        if log_file is None:
            # Get the directory where this file is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to the habit_tracker package directory
            package_dir = os.path.dirname(current_dir)
            # Create logs directory if it doesn't exist
            log_dir = os.path.join(package_dir, 'logs')
            os.makedirs(log_dir, exist_ok=True)
            # Set the full path to the log file
            log_file = os.path.join(log_dir, 'habit_tracker.log')

        # Create a logger with a unique name
        self.logger = logging.getLogger('habit_tracker')
        self.logger.setLevel(logging.INFO)
        
        # Remove any existing handlers to avoid duplicates
        self.logger.handlers = []
        
        # Create a custom JSON formatter
        formatter = jsonlogger.JsonFormatter(
            '%(timestamp)s %(event)s %(habit_id)s %(habit_name)s %(message)s',
            timestamp=True
        )
        
        # Create file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(file_handler)
    
    def log_habit_creation(self, habit_id: int, name: str, periodicity: str):
        """Log habit creation."""
        self.logger.info(
            'Habit created',
            extra={
                'event': 'creation',
                'habit_id': str(habit_id),
                'habit_name': name,
                'periodicity': periodicity,
                'timestamp': datetime.now().isoformat()
            }
        )
    
    def log_habit_completion(self, habit_id: int, name: str):
        """Log habit completion."""
        self.logger.info(
            'Habit completed',
            extra={
                'event': 'completion',
                'habit_id': str(habit_id),
                'habit_name': name,
                'timestamp': datetime.now().isoformat()
            }
        )
    
    def log_habit_deletion(self, habit_id: int, name: str):
        """Log habit deletion."""
        self.logger.info(
            'Habit deleted',
            extra={
                'event': 'deletion',
                'habit_id': str(habit_id),
                'habit_name': name,
                'timestamp': datetime.now().isoformat()
            }
        )
# Habit Tracker

A Python-based habit tracking application that helps users create, maintain, and analyze their daily and weekly habits. Built using object-oriented and functional programming principles.

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🎯 Create and manage up to 10 habits with daily or weekly periodicity
- ✅ Track habit completion and maintain streaks
- 📊 Analyze habit performance with detailed statistics
- 📅 View habit completion patterns in a calendar view
- 📝 Built-in logging for habit activities
- 💾 Local data persistence using JSON storage
- 🔍 Functional programming based analytics
- 🖥️ User-friendly command-line interface

## Predefined Habits

The application comes with 5 predefined habits and example data for a 4-week period:

1. **Morning Exercise** (daily) 
   - 15 minutes of morning stretching and basic exercises
2. **Read a Book** (daily) 
   - Read at least 20 pages
3. **Weekly Planning** (weekly) 
   - Plan goals and tasks for the upcoming week
4. **Drink Water** (daily) 
   - Drink 8 glasses of water
5. **Deep House Cleaning** (weekly) 
   - Thorough cleaning of living space

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/oofpp_habit_tracker.git
cd oofpp_habit_tracker
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package and dependencies:
```bash
pip install -e .
```

## Usage

The habit tracker provides a command-line interface with various commands:

```bash
habit-tracker [OPTIONS] COMMAND [ARGS]...
```

### Available Commands

| Command | Description |
|---------|-------------|
| `add` | Add a new habit to track |
| `list` | List all tracked habits |
| `complete` | Mark a habit as complete |
| `calendar` | Show completion calendar |
| `analyze` | View habit statistics |
| `details` | Show habit details |
| `delete` | Remove a habit |

### Example Usage

```bash
# Add a new daily habit
habit-tracker add
Habit name: "Evening Meditation"
periodicity (daily/weekly) daily

# Complete a habit
habit-tracker complete [OPTIONS] HABIT_ID

# View analytics
habit-tracker analyze

# Show calendar view
habit-tracker calendar
```

## Project Structure

```
habit_tracker/
├── habit_tracker/
│   ├── analytics/        # Analytics and statistics
│   ├── models/          # Core habit classes
│   ├── utils/           # Helper utilities
│   └── cli.py           # Command-line interface
├── example_data/        # Predefined habits
├── tests/              # Test suite
└── data/               # Data storage
```

## Testing

Run the test suite:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=habit_tracker tests/
```

## Technical Details

- Built with Python 3.7+
- Uses Object-Oriented Programming for habit management
- Implements Functional Programming for analytics
- Includes comprehensive unit tests
- Follows PEP 8 style guidelines

## Dependencies

- `click`: Command-line interface creation
- `pytest`: Testing framework
- `python-dateutil`: Date manipulation utilities

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created as part of the Object Oriented and Functional Programming with Python course at IU International University of Applied Sciences.
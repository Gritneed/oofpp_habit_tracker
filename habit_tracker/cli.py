import click
from datetime import datetime
from typing import Optional
from .utils.calendar_view import CalendarView

from .models.habit_manager import HabitManager
from .utils.habit_validator import HabitValidator
from .utils.habit_logger import HabitLogger
from .analytics.analytics_manager import (
    get_completion_rate,
    get_habit_patterns,
    analyze_habit_trends,
    get_streak_analysis
)

habit_manager = HabitManager()
habit_logger = HabitLogger()

def format_habit_info(habit):
    """Format habit information for display."""
    return (
        f"ID: {habit.id}\n"
        f"Name: {habit.name}\n"
        f"Periodicity: {habit.periodicity}\n"
        f"Current streak: {habit.streak_count}\n"
        f"Total completions: {habit.total_check_count}\n"
        f"Created: {habit.creation_date.strftime('%Y-%m-%d')}\n"
        f"Last checked: {habit.last_check_date.strftime('%Y-%m-%d') if habit.last_check_date else 'Never'}\n"
    )

@click.group()
def cli():
    """Habit Tracker - Track and analyze your habits."""
    pass

def show_help():
    """Show help message with example commands."""
    click.echo("""
╔════════════════════════════════════════════════════╗
║               Habit Tracker - Help                 ║
╚════════════════════════════════════════════════════╝

Available Commands:

1. Add a new habit:
   habit-tracker add --name "Morning Exercise" --periodicity daily
   habit-tracker add --name "Weekly Review" --periodicity weekly

2. Complete a habit:
   habit-tracker complete [HABIT_ID]
   Example: habit-tracker complete 1

3. View all habits:
   habit-tracker list

4. View monthly calendar:
   habit-tracker calendar
   habit-tracker calendar --year 2024 --month 3

5. Analyze habits:
   habit-tracker analyze
   habit-tracker analyze --periodicity daily

6. View habit details:
   habit-tracker details [HABIT_ID]
   Example: habit-tracker details 1

7. Delete a habit:
   habit-tracker delete [HABIT_ID]
   Example: habit-tracker delete 1

8. Show this help message:
   habit-tracker
   habit-tracker --help

Options:
  --help  Show this message and exit.

Note: Replace [HABIT_ID] with the actual ID of your habit.
You can see habit IDs using the 'list' command.
""")

@cli.command()
@click.option('--name', prompt='Habit name', help='Name of the habit')
@click.option(
    '--periodicity',
    type=click.Choice(['daily', 'weekly'], case_sensitive=False),
    prompt='Periodicity (daily/weekly)',
    help='How often the habit should be performed'
)
def add(name: str, periodicity: str):
    """Add a new habit to track."""
    try:
        is_valid, error = HabitValidator.validate_habit_creation(name, periodicity)
        if not is_valid:
            click.echo(f"Error: {error}")
            return

        habit = habit_manager.add_habit(name, periodicity)
        habit_logger.log_habit_creation(habit.id, name, periodicity)
        click.echo(f"\nSuccessfully added habit '{name}'")
        click.echo("\nHabit details:")
        click.echo(format_habit_info(habit))
    except ValueError as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.argument('habit_id', type=int)
def complete(habit_id: int):
    """Mark a habit as complete for the current period."""
    habit = habit_manager.get_habit_by_id(habit_id)
    if not habit:
        click.echo(f"Error: No habit found with ID {habit_id}")
        return

    try:
        is_valid, error = HabitValidator.validate_habit_completion(
            habit.last_check_date, 
            habit.periodicity
        )
        if not is_valid:
            click.echo(f"Error: {error}")
            return

        habit.check_off()
        habit_manager.save_data()
        habit_logger.log_habit_completion(habit.id, habit.name)
        click.echo(f"Successfully completed habit '{habit.name}'")
        click.echo(f"Current streak: {habit.streak_count}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.argument('habit_id', type=int)
def delete(habit_id: int):
    """Delete a habit from tracking."""
    habit = habit_manager.get_habit_by_id(habit_id)
    if not habit:
        click.echo(f"Error: No habit found with ID {habit_id}")
        return

    if click.confirm(f"Are you sure you want to delete habit '{habit.name}'?"):
        habit_manager.remove_habit(habit_id)
        habit_logger.log_habit_deletion(habit_id, habit.name)
        click.echo(f"Successfully deleted habit '{habit.name}'")

@cli.command()
def list():
    """List all tracked habits."""
    habits = habit_manager.habits
    if not habits:
        click.echo("No habits are currently being tracked.")
        return

    click.echo("Current habits:\n")
    for habit in habits:
        click.echo(format_habit_info(habit))
        click.echo("-" * 40)

@cli.command()
@click.option(
    '--periodicity',
    type=click.Choice(['daily', 'weekly'], case_sensitive=False),
    help='Filter habits by periodicity'
)
def analyze(periodicity: Optional[str]):
    """Analyze habits and show statistics."""
    habits = habit_manager.habits
    if not habits:
        click.echo("No habits to analyze.")
        return

    if periodicity:
        habits = habit_manager.get_habits_by_periodicity(periodicity)
        if not habits:
            click.echo(f"No {periodicity} habits found.")
            return

    # Prepare data for analysis
    habits_data = []
    for h in habits:
        check_dates = [h.last_check_date] if h.last_check_date else []
        completion_rate = get_completion_rate(
            check_dates,
            h.periodicity,
            h.creation_date
        )
        habits_data.append({
            'name': h.name,
            'periodicity': h.periodicity,
            'completion_rate': completion_rate
        })

    trends = analyze_habit_trends(habits_data)

    click.echo("\nHabit Analysis:")
    click.echo("-" * 40)
    
    click.echo(f"Total habits: {trends['total_habits']}")
    
    if trends['most_successful']:
        click.echo(f"Most successful habit: {trends['most_successful']}")
    if trends['least_successful']:
        click.echo(f"Least successful habit: {trends['least_successful']}")
    
    click.echo("\nHabit breakdown by periodicity:")
    for period, stats in trends['by_periodicity'].items():
        click.echo(f"\n{period.capitalize()}:")
        click.echo(f"  Count: {stats['count']}")
        click.echo(f"  Average completion rate: {stats['avg_completion_rate']:.1f}%")

    if not trends['by_periodicity']:
        click.echo("  No habit data available for analysis")

@cli.command()
@click.argument('habit_id', type=int)
def details(habit_id: int):
    """Show detailed information about a specific habit."""
    habit = habit_manager.get_habit_by_id(habit_id)
    if not habit:
        click.echo(f"Error: No habit found with ID {habit_id}")
        return

    click.echo(f"\nDetailed analysis for '{habit.name}':")
    click.echo("-" * 40)
    
    # Basic info
    click.echo(format_habit_info(habit))
    
    # Streak analysis
    check_dates = [habit.last_check_date] if habit.last_check_date else []
    streak_stats = get_streak_analysis(check_dates, habit.periodicity)
    
    click.echo("\nStreak Analysis:")
    click.echo(f"Current streak: {streak_stats['current_streak']}")
    click.echo(f"Longest streak: {streak_stats['max_streak']}")
    click.echo(f"Average streak: {streak_stats['avg_streak']:.1f}")
    
    # Completion patterns
    if check_dates:
        patterns = get_habit_patterns(check_dates)
        click.echo("\nCompletion Patterns:")
        for period, count in patterns.items():
            click.echo(f"{period.capitalize()}: {count} times")

@cli.command()
@click.option('--year', type=int, default=None, help='Year to display (YYYY)')
@click.option('--month', type=int, default=None, help='Month to display (1-12)')
def calendar(year: Optional[int], month: Optional[int]):
    """Display habit completion calendar."""
    try:
        calendar_view = CalendarView()
        
        # Validate month input if provided
        if month is not None and not (1 <= month <= 12):
            click.echo("Month must be between 1 and 12")
            return
            
        # Get current year/month if not provided
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
            
        # Get all habits
        habits = habit_manager.habits
        if not habits:
            click.echo("No habits to display in calendar.")
            return

        # Generate calendar view
        calendar_output = calendar_view.generate_monthly_view(habits, year, month)
        click.echo(calendar_output)
        
        # Display habit summary
        click.echo(calendar_view.get_habit_summary(habits))
        
        # Display navigation hints
        click.echo("\nNavigation:")
        next_month = month + 1 if month < 12 else 1
        next_year = year + 1 if month == 12 else year
        prev_month = month - 1 if month > 1 else 12
        prev_year = year - 1 if month == 1 else year
        
        click.echo(f"- Next month: habit-tracker calendar --year {next_year} --month {next_month}")
        click.echo(f"- Previous month: habit-tracker calendar --year {prev_year} --month {prev_month}")
        
    except Exception as e:
        click.echo(f"Error displaying calendar: {str(e)}", err=True)

def help():
    """Show detailed help message."""
    show_help()

def main():
    """Main entry point for the CLI."""
    cli()

if __name__ == '__main__':
    main()
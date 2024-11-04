from datetime import datetime, timedelta
import json
import random

def generate_test_data():
    """
    Generate predefined habits with 4 weeks of example data.
    Returns a dictionary containing habits and their completion data.
    """
    # Start date for test data (4 weeks ago from today)
    start_date = datetime.now() - timedelta(weeks=4)
    
    # Predefined habits
    habits = [
        {
            "id": 1,
            "name": "Morning Exercise",
            "periodicity": "daily",
            "creation_date": start_date.isoformat(),
            "description": "15 minutes of morning stretching and basic exercises",
            "is_active": True,
            "completions": []
        },
        {
            "id": 2,
            "name": "Read a Book",
            "periodicity": "daily",
            "creation_date": start_date.isoformat(),
            "description": "Read at least 20 pages",
            "is_active": True,
            "completions": []
        },
        {
            "id": 3,
            "name": "Weekly Planning",
            "periodicity": "weekly",
            "creation_date": start_date.isoformat(),
            "description": "Plan goals and tasks for the upcoming week",
            "is_active": True,
            "completions": []
        },
        {
            "id": 4,
            "name": "Drink Water",
            "periodicity": "daily",
            "creation_date": start_date.isoformat(),
            "description": "Drink 8 glasses of water",
            "is_active": True,
            "completions": []
        },
        {
            "id": 5,
            "name": "Deep House Cleaning",
            "periodicity": "weekly",
            "creation_date": start_date.isoformat(),
            "description": "Thorough cleaning of living space",
            "is_active": True,
            "completions": []
        }
    ]

    # Generate completion data for each habit
    for habit in habits:
        current_date = start_date
        end_date = datetime.now()
        
        while current_date <= end_date:
            # For daily habits
            if habit["periodicity"] == "daily":
                # 80% chance of completion to simulate realistic usage
                if random.random() < 0.8:
                    completion_time = current_date.replace(
                        hour=random.randint(6, 22),
                        minute=random.randint(0, 59)
                    )
                    habit["completions"].append({
                        "date": completion_time.isoformat(),
                        "status": "completed"
                    })
                current_date += timedelta(days=1)
            
            # For weekly habits
            else:
                if current_date.weekday() == 6:  # Sunday
                    # 90% chance of completion for weekly habits
                    if random.random() < 0.9:
                        completion_time = current_date.replace(
                            hour=random.randint(9, 18),
                            minute=random.randint(0, 59)
                        )
                        habit["completions"].append({
                            "date": completion_time.isoformat(),
                            "status": "completed"
                        })
                    current_date += timedelta(days=1)
                else:
                    current_date += timedelta(days=1)

    return habits

def save_test_data(file_path="test_habits_data.json"):
    """
    Generate and save test data to a JSON file.
    
    Args:
        file_path (str): Path where the JSON file will be saved
    """
    habits = generate_test_data()
    
    with open(file_path, 'w') as f:
        json.dump({"habits": habits}, f, indent=2)
    
    print(f"Test data has been generated and saved to {file_path}")
    
    # Print summary of generated data
    print("\nGenerated Habits Summary:")
    for habit in habits:
        print(f"\nHabit: {habit['name']}")
        print(f"Periodicity: {habit['periodicity']}")
        print(f"Total completions: {len(habit['completions'])}")

if __name__ == "__main__":
    save_test_data()
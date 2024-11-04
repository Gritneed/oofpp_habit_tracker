from datetime import datetime, timedelta
from typing import List, Dict, Any
from functools import reduce, partial
from itertools import groupby
from operator import itemgetter

def get_completion_rate(check_dates: List[datetime], periodicity: str, start_date: datetime) -> float:
    """
    Calculate the completion rate of a habit since its start date.
    """
    if not check_dates:
        return 0.0
        
    now = datetime.now()
    days_since_start = max((now - start_date).days, 1)  # Ensure at least 1 day
    
    if periodicity == 'daily':
        expected_count = days_since_start
    else:  # weekly
        expected_count = max(days_since_start // 7, 1)  # Ensure at least 1 week
        
    actual_count = len(set(d.date() for d in check_dates))
    return min((actual_count / expected_count) * 100, 100.0)  # Cap at 100%

def get_habit_patterns(check_dates: List[datetime]) -> Dict[str, int]:
    """
    Analyze patterns in habit completion times.
    """
    if not check_dates:
        return {
            'morning': 0,
            'afternoon': 0,
            'evening': 0,
            'night': 0
        }
        
    # Convert dates to hour buckets
    hour_buckets = list(map(lambda d: d.hour, check_dates))
    
    # Group into time periods
    def categorize_hour(hour: int) -> str:
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        else:
            return "night"
    
    patterns = {'morning': 0, 'afternoon': 0, 'evening': 0, 'night': 0}
    for date in check_dates:
        category = categorize_hour(date.hour)
        patterns[category] += 1
        
    return patterns

def analyze_habit_trends(habits: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze trends across all habits.
    
    Args:
        habits: List of habit dictionaries with completion data
        
    Returns:
        Dictionary with trend analysis
    """
    if not habits:
        return {
            'by_periodicity': {},
            'most_successful': None,
            'least_successful': None,
            'total_habits': 0
        }
    
    # Group habits by periodicity
    habits_by_periodicity = {}
    for habit in habits:
        periodicity = habit.get('periodicity', 'unknown')
        if periodicity not in habits_by_periodicity:
            habits_by_periodicity[periodicity] = []
        habits_by_periodicity[periodicity].append(habit)
    
    # Calculate statistics for each periodicity
    periodicity_stats = {
        period: calculate_group_stats(group)
        for period, group in habits_by_periodicity.items()
    }
    
    # Find most and least successful habits
    habits_with_completion = [h for h in habits if 'completion_rate' in h]
    most_successful = max(habits_with_completion, key=lambda h: h['completion_rate'], default=None)
    least_successful = min(habits_with_completion, key=lambda h: h['completion_rate'], default=None)
    
    return {
        'by_periodicity': periodicity_stats,
        'most_successful': most_successful['name'] if most_successful else None,
        'least_successful': least_successful['name'] if least_successful else None,
        'total_habits': len(habits)
    }

    # Calculate statistics for each group
def calculate_group_stats(habits: List[Dict]) -> Dict[str, Any]:
    """Calculate statistics for a group of habits."""
    if not habits:
        return {
            'count': 0,
            'avg_completion_rate': 0.0
        }
    
    total_completion_rate = sum(h.get('completion_rate', 0) for h in habits)
    count = len(habits)
    
    return {
        'count': count,
        'avg_completion_rate': total_completion_rate / count if count > 0 else 0.0
    }

def get_streak_analysis(check_dates: List[datetime], periodicity: str) -> Dict[str, Any]:
    """
    Analyze streak patterns for a habit.
    """
    if not check_dates:
        return {
            'current_streak': 0,
            'max_streak': 0,
            'avg_streak': 0.0
        }
    
    sorted_dates = sorted(check_dates)
    current_streak = max_streak = 0
    all_streaks = []
    
    for i in range(len(sorted_dates)):
        if i == 0:
            current_streak = 1
            continue
            
        date_diff = (sorted_dates[i] - sorted_dates[i-1]).days
        expected_diff = 1 if periodicity == 'daily' else 7
        
        if date_diff == expected_diff:
            current_streak += 1
        else:
            all_streaks.append(current_streak)
            current_streak = 1
            
        max_streak = max(max_streak, current_streak)
    
    all_streaks.append(current_streak)
    
    return {
        'current_streak': current_streak,
        'max_streak': max_streak,
        'avg_streak': sum(all_streaks) / len(all_streaks) if all_streaks else 0.0
    }
    
    # Calculate gaps between completions
    def get_gap(dates):
        return (dates[1] - dates[0]).days
        
    date_pairs = zip(sorted_dates[:-1], sorted_dates[1:])
    gaps = list(map(get_gap, date_pairs))
    
    # Identify streaks
    def is_streak(gap):
        return gap == 1 if periodicity == 'daily' else gap == 7
        
    streak_flags = list(map(is_streak, gaps))
    
    # Calculate streak lengths
    def count_streak(acc, flag):
        current, max_streak, streaks = acc
        if flag:
            current += 1
            return (current, max(max_streak, current), streaks + [current])
        else:
            return (0, max_streak, streaks + [current])
            
    initial = (0, 0, [])
    final_current, max_streak, all_streaks = reduce(count_streak, streak_flags, initial)
    
    return {
        'current_streak': final_current,
        'max_streak': max_streak,
        'avg_streak': sum(all_streaks) / len(all_streaks) if all_streaks else 0
    }
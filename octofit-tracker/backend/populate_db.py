import os
import sys
import django
from datetime import datetime, timedelta
import random

# Setup Django environment
sys.path.append('/workspaces/skills-build-applications-w-copilot-agent-mode/octofit-tracker/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
django.setup()

from django.contrib.auth.models import User
from fitness.models import UserProfile, Activity, Team, WorkoutSuggestion

def populate_database():
    print("Starting database population...")
    
    # Create users
    print("\nCreating users...")
    users_data = [
        {'username': 'alice', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Johnson'},
        {'username': 'bob', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Smith'},
        {'username': 'charlie', 'email': 'charlie@example.com', 'first_name': 'Charlie', 'last_name': 'Brown'},
        {'username': 'diana', 'email': 'diana@example.com', 'first_name': 'Diana', 'last_name': 'Williams'},
    ]
    
    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name']
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"  Created user: {user.username}")
        else:
            print(f"  User already exists: {user.username}")
        users.append(user)
    
    # Create user profiles
    print("\nCreating user profiles...")
    profile_data = [
        {'user': users[0], 'bio': 'Marathon enthusiast', 'fitness_goal': 'Run a sub-4 hour marathon'},
        {'user': users[1], 'bio': 'Gym lover and weightlifter', 'fitness_goal': 'Bench press 200 lbs'},
        {'user': users[2], 'bio': 'Yoga and mindfulness practitioner', 'fitness_goal': 'Practice yoga daily'},
        {'user': users[3], 'bio': 'Cycling enthusiast', 'fitness_goal': 'Complete a century ride'},
    ]
    
    for data in profile_data:
        profile, created = UserProfile.objects.get_or_create(
            user=data['user'],
            defaults={'bio': data['bio'], 'fitness_goal': data['fitness_goal']}
        )
        if created:
            print(f"  Created profile for: {data['user'].username}")
        else:
            print(f"  Profile already exists for: {data['user'].username}")
    
    # Create activities
    print("\nCreating activities...")
    activity_types = ['running', 'cycling', 'swimming', 'walking', 'gym', 'yoga']
    for i in range(20):
        user = random.choice(users)
        activity_type = random.choice(activity_types)
        activity_date = datetime.now() - timedelta(days=random.randint(1, 30))
        
        activity, created = Activity.objects.get_or_create(
            user=user,
            activity_type=activity_type,
            date=activity_date,
            defaults={
                'duration': random.randint(20, 120),
                'distance': round(random.uniform(1, 20), 2) if activity_type in ['running', 'cycling', 'walking'] else None,
                'calories': random.randint(100, 800),
                'notes': f'Great {activity_type} session!'
            }
        )
        if created:
            print(f"  Created activity: {user.username} - {activity_type}")
    
    # Create teams
    print("\nCreating teams...")
    teams_data = [
        {'name': 'Morning Warriors', 'description': 'Early bird workout team', 'creator': users[0], 'members': [users[0], users[1]]},
        {'name': 'Weekend Warriors', 'description': 'Weekend fitness enthusiasts', 'creator': users[2], 'members': [users[2], users[3]]},
        {'name': 'Cardio Kings', 'description': 'Focus on cardio activities', 'creator': users[1], 'members': [users[0], users[1], users[3]]},
    ]
    
    for team_data in teams_data:
        team, created = Team.objects.get_or_create(
            name=team_data['name'],
            defaults={
                'description': team_data['description'],
                'created_by': team_data['creator']
            }
        )
        if created:
            team.members.set(team_data['members'])
            print(f"  Created team: {team.name}")
        else:
            print(f"  Team already exists: {team.name}")
    
    # Create workout suggestions
    print("\nCreating workout suggestions...")
    suggestions_data = [
        {
            'title': '5K Running Plan',
            'description': 'Build up to running 5 kilometers in 8 weeks',
            'activity_type': 'running',
            'difficulty': 'beginner',
            'duration': 30,
            'calories_estimate': 300
        },
        {
            'title': 'HIIT Cardio Blast',
            'description': 'High-intensity interval training for maximum calorie burn',
            'activity_type': 'gym',
            'difficulty': 'advanced',
            'duration': 45,
            'calories_estimate': 500
        },
        {
            'title': 'Morning Yoga Flow',
            'description': 'Gentle yoga routine to start your day',
            'activity_type': 'yoga',
            'difficulty': 'beginner',
            'duration': 20,
            'calories_estimate': 100
        },
        {
            'title': 'Cycling Endurance',
            'description': 'Build stamina with steady-state cycling',
            'activity_type': 'cycling',
            'difficulty': 'intermediate',
            'duration': 60,
            'calories_estimate': 450
        },
        {
            'title': 'Swimming Technique',
            'description': 'Focus on improving your freestyle stroke',
            'activity_type': 'swimming',
            'difficulty': 'intermediate',
            'duration': 40,
            'calories_estimate': 350
        },
    ]
    
    for suggestion_data in suggestions_data:
        suggestion, created = WorkoutSuggestion.objects.get_or_create(
            title=suggestion_data['title'],
            defaults=suggestion_data
        )
        if created:
            print(f"  Created workout suggestion: {suggestion.title}")
        else:
            print(f"  Workout suggestion already exists: {suggestion.title}")
    
    print("\n✅ Database population complete!")
    print(f"\nSummary:")
    print(f"  Users: {User.objects.count()}")
    print(f"  User Profiles: {UserProfile.objects.count()}")
    print(f"  Activities: {Activity.objects.count()}")
    print(f"  Teams: {Team.objects.count()}")
    print(f"  Workout Suggestions: {WorkoutSuggestion.objects.count()}")

if __name__ == '__main__':
    populate_database()

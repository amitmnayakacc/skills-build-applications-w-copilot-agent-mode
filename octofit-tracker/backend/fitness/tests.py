from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime, timedelta
from .models import UserProfile, Activity, Team, WorkoutSuggestion


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_user_profile(self):
        profile = UserProfile.objects.create(
            user=self.user,
            bio='Test bio',
            fitness_goal='Run 5K'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(str(profile), f"{self.user.username}'s profile")


class ActivityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_activity(self):
        activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration=30,
            distance=5.0,
            calories=300,
            date=datetime.now()
        )
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.activity_type, 'running')
        self.assertEqual(activity.duration, 30)


class TeamModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
    
    def test_create_team(self):
        team = Team.objects.create(
            name='Test Team',
            description='Test description',
            created_by=self.user1
        )
        team.members.add(self.user1, self.user2)
        
        self.assertEqual(team.name, 'Test Team')
        self.assertEqual(team.members.count(), 2)
        self.assertEqual(str(team), 'Test Team')


class WorkoutSuggestionModelTest(TestCase):
    def test_create_workout_suggestion(self):
        workout = WorkoutSuggestion.objects.create(
            title='Morning Run',
            description='Easy 5K run',
            activity_type='running',
            difficulty='beginner',
            duration=30,
            calories_estimate=300
        )
        self.assertEqual(workout.title, 'Morning Run')
        self.assertEqual(workout.difficulty, 'beginner')


class ActivityAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.activity_data = {
            'user_id': self.user.id,
            'activity_type': 'running',
            'duration': 30,
            'distance': 5.0,
            'calories': 300,
            'date': datetime.now().isoformat(),
            'notes': 'Great run!'
        }
    
    def test_create_activity(self):
        response = self.client.post('/api/activities/', self.activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
        self.assertEqual(Activity.objects.get().activity_type, 'running')
    
    def test_get_activities(self):
        Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration=30,
            date=datetime.now()
        )
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_filter_activities_by_user(self):
        Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration=30,
            date=datetime.now()
        )
        response = self.client.get(f'/api/activities/?user_id={self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TeamAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.team_data = {
            'name': 'Test Team',
            'description': 'Test description',
            'created_by_id': self.user1.id,
            'member_ids': [self.user1.id, self.user2.id]
        }
    
    def test_create_team(self):
        response = self.client.post('/api/teams/', self.team_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
        team = Team.objects.get()
        self.assertEqual(team.members.count(), 2)
    
    def test_get_teams(self):
        Team.objects.create(
            name='Test Team',
            created_by=self.user1
        )
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        
        # Create activities for users
        Activity.objects.create(
            user=self.user1,
            activity_type='running',
            duration=30,
            calories=300,
            date=datetime.now()
        )
        Activity.objects.create(
            user=self.user2,
            activity_type='cycling',
            duration=45,
            calories=400,
            date=datetime.now()
        )
    
    def test_global_leaderboard(self):
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # user2 should be ranked first (400 calories > 300 calories)
        self.assertEqual(response.data[0]['rank'], 1)
        self.assertEqual(response.data[0]['user']['username'], 'user2')


class WorkoutSuggestionAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        WorkoutSuggestion.objects.create(
            title='5K Run',
            description='Beginner running plan',
            activity_type='running',
            difficulty='beginner',
            duration=30,
            calories_estimate=300
        )
    
    def test_get_workout_suggestions(self):
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_filter_by_difficulty(self):
        response = self.client.get('/api/workouts/?difficulty=beginner')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


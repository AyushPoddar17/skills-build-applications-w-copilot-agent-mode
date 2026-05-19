from django.test import TestCase
from .models import User, Team, Workout, Activity, Leaderboard

class ModelTests(TestCase):
    def setUp(self):
        team = Team.objects.create(name='Test Team', description='A test team')
        user = User.objects.create(name='Test User', email='test@example.com', team=team)
        workout = Workout.objects.create(name='Test Workout', description='A test workout', difficulty='Easy')
        activity = Activity.objects.create(user=user, workout=workout, duration=30, calories=200)
        Leaderboard.objects.create(team=team, points=100)

    def test_user(self):
        self.assertEqual(User.objects.count(), 1)

    def test_team(self):
        self.assertEqual(Team.objects.count(), 1)

    def test_workout(self):
        self.assertEqual(Workout.objects.count(), 1)

    def test_activity(self):
        self.assertEqual(Activity.objects.count(), 1)

    def test_leaderboard(self):
        self.assertEqual(Leaderboard.objects.count(), 1)

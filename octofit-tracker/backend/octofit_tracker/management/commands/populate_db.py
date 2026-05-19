from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import connection
from pymongo import ASCENDING

from django.contrib.auth import get_user_model
from django.db import connections

import random

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Connecting to MongoDB...'))
        db = connection.cursor().db_conn.client['octofit_db']

        # Drop collections if they exist
        for col in ['users', 'teams', 'activities', 'leaderboard', 'workouts']:
            db[col].drop()

        # Create unique index on email for users
        db['users'].create_index([('email', ASCENDING)], unique=True)

        # Teams
        teams = [
            {'name': 'Team Marvel', 'description': 'Marvel superheroes'},
            {'name': 'Team DC', 'description': 'DC superheroes'},
        ]
        team_ids = db['teams'].insert_many(teams).inserted_ids

        # Users
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': team_ids[0]},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': team_ids[0]},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': team_ids[0]},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': team_ids[1]},
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': team_ids[1]},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': team_ids[1]},
        ]
        user_ids = db['users'].insert_many(users).inserted_ids

        # Workouts
        workouts = [
            {'name': 'Push Ups', 'description': 'Upper body workout', 'difficulty': 'Easy'},
            {'name': 'Running', 'description': 'Cardio workout', 'difficulty': 'Medium'},
            {'name': 'Deadlift', 'description': 'Strength workout', 'difficulty': 'Hard'},
        ]
        workout_ids = db['workouts'].insert_many(workouts).inserted_ids

        # Activities
        activities = []
        for user_id in user_ids:
            for workout_id in workout_ids:
                activities.append({
                    'user': user_id,
                    'workout': workout_id,
                    'duration': random.randint(10, 60),
                    'calories': random.randint(100, 500),
                })
        db['activities'].insert_many(activities)

        # Leaderboard
        leaderboard = []
        for team_id in team_ids:
            leaderboard.append({
                'team': team_id,
                'points': random.randint(1000, 5000),
            })
        db['leaderboard'].insert_many(leaderboard)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data!'))

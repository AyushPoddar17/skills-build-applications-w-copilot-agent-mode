from django.contrib import admin
from .models import User, Team, Workout, Activity, Leaderboard

admin.site.register(User)
admin.site.register(Team)
admin.site.register(Workout)
admin.site.register(Activity)
admin.site.register(Leaderboard)

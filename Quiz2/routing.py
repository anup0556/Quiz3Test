from django.urls import re_path
from leaderboard.consumers import LeaderboardConsumer

websocket_urlpatterns = [
    re_path(r'ws/leaderboard/$', LeaderboardConsumer.as_asgi()),
]
from rest_framework import serializers
from .models import LeaderBoard

class LeaderBoardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = LeaderBoard
        fields = ['username', 'score', 'total_questions_attempted', 'last_played']
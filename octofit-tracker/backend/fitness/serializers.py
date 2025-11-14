from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Activity, Team, WorkoutSuggestion


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'user_id', 'bio', 'fitness_goal', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    
    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'user_id', 'activity_type', 'activity_type_display',
            'duration', 'distance', 'calories', 'notes', 'date', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class TeamSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.IntegerField(write_only=True)
    members = UserSerializer(many=True, read_only=True)
    member_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    member_count = serializers.SerializerMethodField()
    total_activities = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'created_by', 'created_by_id',
            'members', 'member_ids', 'member_count', 'total_activities',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_total_activities(self, obj):
        return obj.total_activities()
    
    def create(self, validated_data):
        member_ids = validated_data.pop('member_ids', [])
        team = Team.objects.create(**validated_data)
        if member_ids:
            team.members.set(User.objects.filter(id__in=member_ids))
        return team
    
    def update(self, instance, validated_data):
        member_ids = validated_data.pop('member_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if member_ids is not None:
            instance.members.set(User.objects.filter(id__in=member_ids))
        
        return instance


class WorkoutSuggestionSerializer(serializers.ModelSerializer):
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    
    class Meta:
        model = WorkoutSuggestion
        fields = [
            'id', 'title', 'description', 'activity_type', 'difficulty',
            'difficulty_display', 'duration', 'calories_estimate', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class LeaderboardSerializer(serializers.Serializer):
    user = UserSerializer()
    total_activities = serializers.IntegerField()
    total_duration = serializers.IntegerField()
    total_distance = serializers.FloatField()
    total_calories = serializers.IntegerField()
    rank = serializers.IntegerField()

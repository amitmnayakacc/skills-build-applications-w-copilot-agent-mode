from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from .models import UserProfile, Activity, Team, WorkoutSuggestion
from .serializers import (
    UserSerializer, UserProfileSerializer, ActivitySerializer,
    TeamSerializer, WorkoutSuggestionSerializer, LeaderboardSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            profile = UserProfile.objects.get(user_id=user_id)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        queryset = Activity.objects.all()
        user_id = self.request.query_params.get('user_id')
        activity_type = self.request.query_params.get('activity_type')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        limit = int(request.query_params.get('limit', 10))
        activities = self.get_queryset()[:limit]
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        activities = Activity.objects.filter(user_id=user_id)
        stats = activities.aggregate(
            total_activities=Count('id'),
            total_duration=Sum('duration'),
            total_distance=Sum('distance'),
            total_calories=Sum('calories')
        )
        
        return Response(stats)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    def get_queryset(self):
        queryset = Team.objects.all()
        user_id = self.request.query_params.get('user_id')
        
        if user_id:
            queryset = queryset.filter(members__id=user_id)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            team.members.add(user)
            serializer = self.get_serializer(team)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            team.members.remove(user)
            serializer = self.get_serializer(team)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class WorkoutSuggestionViewSet(viewsets.ModelViewSet):
    queryset = WorkoutSuggestion.objects.all()
    serializer_class = WorkoutSuggestionSerializer
    
    def get_queryset(self):
        queryset = WorkoutSuggestion.objects.all()
        difficulty = self.request.query_params.get('difficulty')
        activity_type = self.request.query_params.get('activity_type')
        
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def random(self, request):
        count = int(request.query_params.get('count', 3))
        suggestions = self.get_queryset().order_by('?')[:count]
        serializer = self.get_serializer(suggestions, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def global_leaderboard(self, request):
        # Aggregate activity stats per user
        user_stats = User.objects.annotate(
            total_activities=Count('activities'),
            total_duration=Sum('activities__duration'),
            total_distance=Sum('activities__distance'),
            total_calories=Sum('activities__calories')
        ).filter(total_activities__gt=0).order_by('-total_calories')
        
        # Add rank
        leaderboard_data = []
        for rank, user in enumerate(user_stats, start=1):
            leaderboard_data.append({
                'user': user,
                'total_activities': user.total_activities or 0,
                'total_duration': user.total_duration or 0,
                'total_distance': user.total_distance or 0.0,
                'total_calories': user.total_calories or 0,
                'rank': rank
            })
        
        serializer = LeaderboardSerializer(leaderboard_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def team_leaderboard(self, request):
        team_id = request.query_params.get('team_id')
        if not team_id:
            return Response(
                {'error': 'team_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            team = Team.objects.get(id=team_id)
            user_stats = User.objects.filter(teams=team).annotate(
                total_activities=Count('activities'),
                total_duration=Sum('activities__duration'),
                total_distance=Sum('activities__distance'),
                total_calories=Sum('activities__calories')
            ).filter(total_activities__gt=0).order_by('-total_calories')
            
            # Add rank
            leaderboard_data = []
            for rank, user in enumerate(user_stats, start=1):
                leaderboard_data.append({
                    'user': user,
                    'total_activities': user.total_activities or 0,
                    'total_duration': user.total_duration or 0,
                    'total_distance': user.total_distance or 0.0,
                    'total_calories': user.total_calories or 0,
                    'rank': rank
                })
            
            serializer = LeaderboardSerializer(leaderboard_data, many=True)
            return Response(serializer.data)
        except Team.DoesNotExist:
            return Response(
                {'error': 'Team not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def list(self, request):
        return self.global_leaderboard(request)


from django.contrib import admin
from .models import UserProfile, Activity, Team, WorkoutSuggestion


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'fitness_goal', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'fitness_goal']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'duration', 'distance', 'calories', 'date', 'created_at']
    search_fields = ['user__username', 'activity_type', 'notes']
    list_filter = ['activity_type', 'date', 'created_at']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'member_count', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'created_by__username']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['members']
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'


@admin.register(WorkoutSuggestion)
class WorkoutSuggestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity_type', 'difficulty', 'duration', 'calories_estimate', 'created_at']
    search_fields = ['title', 'description', 'activity_type']
    list_filter = ['difficulty', 'activity_type', 'created_at']
    readonly_fields = ['created_at']


from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    fitness_goal = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('walking', 'Walking'),
        ('gym', 'Gym'),
        ('yoga', 'Yoga'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    duration = models.IntegerField(help_text="Duration in minutes")
    distance = models.FloatField(help_text="Distance in kilometers", null=True, blank=True)
    calories = models.IntegerField(help_text="Calories burned", null=True, blank=True)
    notes = models.TextField(blank=True)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"

class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name='teams')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def total_activities(self):
        return Activity.objects.filter(user__in=self.members.all()).count()

class WorkoutSuggestion(models.Model):
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_type = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    duration = models.IntegerField(help_text="Duration in minutes")
    calories_estimate = models.IntegerField(help_text="Estimated calories burned")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.difficulty})"


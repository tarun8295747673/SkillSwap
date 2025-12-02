from rest_framework import serializers
from .models import TimeBankUser, TimeEntry

class TimeBankUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = TimeBankUser
        fields = ['username', 'email', 'password', 'hours_available']

    def create(self, validated_data):
        user = TimeBankUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class TimeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        fields = ['id', 'user', 'hours', 'description', 'created_at']
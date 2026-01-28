from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message, ModerationResult, Report, ModerationAction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ModerationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModerationResult
        fields = ['id', 'toxicity', 'severe_toxicity', 'obscene', 'threat', 'insult', 'identity_attack', 'category',
                  'analyzed_at']


class MessageSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    moderation_result = ModerationResultSerializer(read_only=True)
    reports_count = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'author', 'content', 'status', 'created_at', 'updated_at', 'moderation_result', 'reports_count']
        read_only_fields = ['status', 'created_at', 'updated_at']

    def get_reports_count(self, obj):
        return obj.reports.count()


class ReportSerializer(serializers.ModelSerializer):
    reporter = UserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'message', 'reporter', 'reason', 'description', 'created_at']
        read_only_fields = ['created_at']


class ModerationActionSerializer(serializers.ModelSerializer):
    moderator = UserSerializer(read_only=True)

    class Meta:
        model = ModerationAction
        fields = ['id', 'message', 'moderator', 'action', 'reason', 'created_at']
        read_only_fields = ['created_at']
from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approuve'),
        ('pending', 'En attente'),
        ('flagged', 'Signale'),
        ('rejected', 'Rejete'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username} - {self.content[:50]}"


class ModerationResult(models.Model):
    CATEGORY_CHOICES = [
        ('safe', 'Sur'),
        ('toxic', 'Toxique'),
        ('obscene', 'Obscene'),
        ('threat', 'Menace'),
        ('insult', 'Insulte'),
        ('hate', 'Haineux'),
    ]

    message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name='moderation_result')
    toxicity = models.FloatField(default=0.0)
    severe_toxicity = models.FloatField(default=0.0)
    obscene = models.FloatField(default=0.0)
    threat = models.FloatField(default=0.0)
    insult = models.FloatField(default=0.0)
    identity_attack = models.FloatField(default=0.0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='safe')
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analyse {self.message.id} - {self.category}"


class Report(models.Model):
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('harassment', 'Harcelement'),
        ('hate_speech', 'Discours haineux'),
        ('inappropriate', 'Inapproprie'),
        ('violence', 'Violence'),
        ('other', 'Autre'),
    ]

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['message', 'reporter']

    def __str__(self):
        return f"Report par {self.reporter.username}"


class ModerationAction(models.Model):
    ACTION_CHOICES = [
        ('approve', 'Approuve'),
        ('reject', 'Rejete'),
        ('restore', 'Restaure'),
    ]

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='moderation_actions')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderation_actions')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.moderator.username} - {self.action}"

# Create your models here.

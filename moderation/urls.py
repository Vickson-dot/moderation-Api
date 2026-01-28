from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, ModerationViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'moderation', ModerationViewSet, basename='moderation')

urlpatterns = [
    path('', include(router.urls)),
]
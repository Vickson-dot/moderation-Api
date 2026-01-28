from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count, Q, Avg
from .models import Message, Report, ModerationAction
from .serializers import MessageSerializer, ReportSerializer, ModerationActionSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], url_path='report')
    def report_message(self, request, pk=None):
        message = self.get_object()

        if Report.objects.filter(message=message, reporter=request.user).exists():
            return Response({'error': 'Deja signale'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(message=message, reporter=request.user)

            if message.reports.count() >= 3 and message.status == 'approved':
                message.status = 'flagged'
                message.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModerationViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def list(self, request):
        messages = Message.objects.filter(status='flagged').select_related('author', 'moderation_result')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='pending')
    def pending_messages(self, request):
        messages = Message.objects.filter(Q(status='pending') | Q(status='flagged')).select_related('author',
                                                                                                    'moderation_result')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve_message(self, request, pk=None):
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({'error': 'Message introuvable'}, status=status.HTTP_404_NOT_FOUND)

        message.status = 'approved'
        message.save()

        ModerationAction.objects.create(
            message=message,
            moderator=request.user,
            action='approve',
            reason=request.data.get('reason', '')
        )

        return Response({'message': 'Approuve', 'data': MessageSerializer(message).data})

    @action(detail=True, methods=['post'], url_path='reject')
    def reject_message(self, request, pk=None):
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({'error': 'Message introuvable'}, status=status.HTTP_404_NOT_FOUND)

        message.status = 'rejected'
        message.save()

        ModerationAction.objects.create(
            message=message,
            moderator=request.user,
            action='reject',
            reason=request.data.get('reason', '')
        )

        return Response({'message': 'Rejete', 'data': MessageSerializer(message).data})

    @action(detail=False, methods=['get'], url_path='stats')
    def statistics(self, request):
        total_messages = Message.objects.count()

        stats = {
            'total_messages': total_messages,
            'approved': Message.objects.filter(status='approved').count(),
            'pending': Message.objects.filter(status='pending').count(),
            'flagged': Message.objects.filter(status='flagged').count(),
            'rejected': Message.objects.filter(status='rejected').count(),
            'total_reports': Report.objects.count(),
            'moderation_actions': ModerationAction.objects.count(),
        }

        return Response(stats)

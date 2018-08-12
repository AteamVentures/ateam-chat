# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import DynamicFieldsModelSerializer
from api.chat.models import Message
from api.chat.serializers import MessageSerializer


@csrf_exempt
class ChatViewSet(DynamicFieldsModelSerializer):
    """
    /chat
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=True)
    def read(self, request, pk):
        message = self.get_object()
        message.read()
        return Response(status=status.HTTP_200_OK)

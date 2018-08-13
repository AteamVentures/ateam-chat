# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import filters, permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from api.users.models import User
from api.users.signals import user_registered
from .serializers import UserSerializer


class UsersViewSet(ModelViewSet):
    """
    /users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_url_kwarg = 'username'
    lookup_field = 'username'

    def perform_create(self, serializer):
        instance = serializer.save()
        user_registered.send(
            sender=self.__class__, request=self.request, user=instance
        )
        return instance

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (permissions.AllowAny,)
        return super(UsersViewSet, self).get_permissions()

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

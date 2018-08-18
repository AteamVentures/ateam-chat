# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import filters, mixins, permissions
from rest_framework.viewsets import GenericViewSet

from api.users.models import User
from api.users.signals import user_registered
from .serializers import UserSerializer


class UsersViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
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

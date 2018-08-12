# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import validators
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.serializers import DynamicFieldsModelSerializer
from api.users.models import User


class UserSerializer(DynamicFieldsModelSerializer):
    username = serializers.CharField(
        min_length=5, max_length=32,
        validators=[
            validators.RegexValidator(
                r'^(?!_)[a-zA-Z0-9_]+$',
                _("Enter alphabet, digits and _ only"),
                'invalid'
            ),
            UniqueValidator(queryset=User.objects.all())
        ])
    password = serializers.CharField(min_length=6, max_length=20, write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'name', 'phone', 'email', 'date_joined'
        )
        retrieve_fields = (
            'username', 'name', 'phone', 'email',
        )
        read_only_fields = ('date_joined')

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance


class UserSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'type', 'name')

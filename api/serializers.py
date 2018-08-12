# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = None
        try:
            if hasattr(kwargs['context']['view'], 'action'):
                action = self.context['view'].action
                if action == 'retrieve' and hasattr(self.Meta, 'retrieve_fields'):
                    fields = self.Meta.retrieve_fields
                elif action == 'list' and hasattr(self.Meta, 'list_fields'):
                    fields = self.Meta.list_fields
        except:
            pass

        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

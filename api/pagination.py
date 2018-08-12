# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from base64 import b64encode
from collections import OrderedDict

from urllib.parse import urlparse
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 500

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return page_number


class CustomCursorPagination(CursorPagination):
    cursor_query_param = 'page'

    def encode_cursor(self, cursor):
        """
        Given a Cursor instance, return an url with encoded cursor.
        """
        tokens = {}
        if cursor.offset != 0:
            tokens['o'] = str(cursor.offset)
        if cursor.reverse:
            tokens['r'] = '1'
        if cursor.position is not None:
            tokens['p'] = cursor.position

        querystring = urlparse.urlencode(tokens, doseq=True)
        return b64encode(querystring.encode('ascii')).decode('ascii')

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', 1),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class DefaultCursorPagination(CustomCursorPagination):
    page_size = 10


class IdCursorPagination(CustomCursorPagination):
    page_size = 10
    ordering = '-id'


class LargeCursorPagination(CustomCursorPagination):
    page_size = 500


class StandardCursorPagination(CursorPagination):
    cursor_query_param = 'page'
    page_size = 10
    ordering = '-id'

    def encode_cursor(self, cursor):
        """
        Given a Cursor instance, return an url with encoded cursor.
        """
        tokens = {}
        if cursor.offset != 0:
            tokens['o'] = str(cursor.offset)
        if cursor.reverse:
            tokens['r'] = '1'
        if cursor.position is not None:
            tokens['p'] = cursor.position

        querystring = urlparse.urlencode(tokens, doseq=True)
        return b64encode(querystring.encode('ascii')).decode('ascii')

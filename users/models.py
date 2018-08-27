# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import models as auth_models
from django.contrib.auth.models import UserManager as AuthUserManager, User
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):

    username = models.CharField(
        verbose_name=_('username'), unique=True,
        max_length=32,
        help_text='필수입니다. 영문소문자, 숫자와 밑줄(_)만 입력가능합니다.',
        validators=[
            validators.MinLengthValidator(3),
            validators.MaxLengthValidator(32),
            validators.RegexValidator(
                r'^(?!_)[a-zA-Z0-9_]+$',
                '영문소문자, 숫자와 밑줄(_)만 입력가능합니다.',
                'invalid')])
    name = models.CharField(verbose_name='이름', max_length=50)
    display_name = models.CharField(verbose_name='닉네임', max_length=20, blank=True)
    email = models.EmailField(verbose_name='이메일', max_length=190, db_index=True)
    phone = models.CharField('연락처', max_length=30, db_index=True,
                             validators=[validators.RegexValidator(
                                 r'^[0-9]+$',
                                 '숫자만 입력 가능합니다.',
                                 'invalid')])
    date_joined = models.DateTimeField(verbose_name='가입일', default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = AuthUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        is_new = not self.id
        if is_new:
            self.subscription_updated_at = self.date_joined
        super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        return self.name.strip()

    def get_short_name(self):
        return self.name.strip()

# Models for default DB
# (Used by NagiFront, not NDOUtils)

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from .customfields import JSONField 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dashboard_setting = JSONField()

    def get_dashboard_setting(self):
        return self.dashboard_setting

    def modify_dashboard_setting(self, new_setting):
        self.dashboard_setting = new_setting
        self.save()

    def __str__(self):
        return str(self.user)


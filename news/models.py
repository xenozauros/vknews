# -*- coding: utf-8 -*-
from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=30, primary_key=True)


class Spammers(models.Model):
    user = models.ForeignKey(User)
    spammer_id = models.CharField(max_length=30)


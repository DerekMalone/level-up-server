from django.db import models

class GameType(models.Model):

    label = models.TextField(max_length=55)
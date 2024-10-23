from django.db import models
from datetime import datetime


class ScrapyData(models.Model):
    data_type = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    published_date = models.DateField(default=datetime.now())
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the time when the object is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update the time whenever the object is saved

    def __str__(self):
        return '_'


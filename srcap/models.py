from django.db import models
from datetime import datetime



class ScrapyDataManager(models.Manager):
    def data_update(self, data_id, data):
        return self.filter(id=data_id).update(**data)


class ScrapyData(models.Model):
    data_type = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    published_date = models.DateField(default=datetime.now())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ScrapyDataManager()

    def __str__(self):
        return '_'


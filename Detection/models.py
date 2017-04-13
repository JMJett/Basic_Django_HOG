from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class Video(models.Model):
    filename = models.CharField(max_length=200)
    human = models.BooleanField(default=False)
    timestamp = models.DateTimeField('Time Analysed')

    def __str__(self):
        return self.filename

    def detected_human(self):
        return self.human

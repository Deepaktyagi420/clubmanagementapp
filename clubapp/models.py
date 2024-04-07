from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from datetime import datetime
from django.utils import timezone


class ActivitiesModel(models.Model):
    activity_img = models.ImageField(upload_to='static')
    activity_name = models.CharField(max_length=256)
    activity_desc = models.TextField()
    activity_price = models.FloatField()


class BookedActivity(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    activity = models.ForeignKey(ActivitiesModel, models.CASCADE)
    activity_slot =  models.CharField(max_length=256, blank=True, null=True)
    date_of_booking = models.DateField(default=timezone.now)
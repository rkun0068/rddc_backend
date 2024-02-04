from django.db import models
from django.utils.timezone import now


# Create your models here.

class DetectionResult(models.Model):
    img_url = models.TextField()
    result = models.TextField()
    created = models.DateTimeField(default=now)

    class Meta:
        managed = False
        db_table = "detection_result"

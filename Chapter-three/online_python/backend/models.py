from django.db import models

class Code(models.Model):
    name = models.CharField(max_length=20, blank=True)
    code = models.TextField()
    
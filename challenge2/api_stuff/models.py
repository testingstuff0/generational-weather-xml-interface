from django.db import models
from django.core.validators import RegexValidator

class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    type = models.CharField(max_length=3, choices=[('xml', 'xml file')])
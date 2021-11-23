from django.db import models

# Create your models here.
class EmailModel(models.Model):
    email = models.EmailField()

class CodeModel(models.Model):
    code = models.TextField()


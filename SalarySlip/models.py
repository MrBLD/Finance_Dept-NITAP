from fileinput import filename
import os
from os import path
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Teacher(User):
    Employee_id = models.IntegerField(primary_key=True)
    image = models.ImageField(upload_to='media/Images',blank=True, null=True)
    Degisnation = models.CharField(max_length=100, default="Employee")

    def save(self, *args, **kwargs):
        if self.image:
            ext = path.splitext(filename)[1]
            self.image.name = f"{self.first_name}_{self.last_name}_{self.Degisnation}{ext}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name

class Report(models.Model):
    month = models.CharField(max_length=25)
    year = models.CharField(max_length=4)
    excel = models.FileField(upload_to='media/AllMonthData')

    def save(self, *args, **kwargs):
        if self.excel:
            self.excel.name = f"{self.month}_{self.year}.xlsx"
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.excel:
            os.remove(self.excel.path)
        super(Report, self).delete(*args, **kwargs)

    def getName(self):
        return f'{self.month}_{self.year}'
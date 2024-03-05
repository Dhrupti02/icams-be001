from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.Course)
admin.site.register(models.EnrolledUsers)
admin.site.register(models.Document)
admin.site.register(models.DocumentFiles)
admin.site.register(models.Task)
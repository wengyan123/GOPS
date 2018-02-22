from django.contrib import admin

# Register your models here.

# 
# https://stackoverflow.com/questions/10672987/how-to-properly-configure-djcelery-results-backend-to-database
from djcelery.models import TaskMeta
class TaskMetaAdmin(admin.ModelAdmin):
    readonly_fields = ('result',)
admin.site.register(TaskMeta, TaskMetaAdmin)

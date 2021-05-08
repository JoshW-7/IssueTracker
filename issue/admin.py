from django.contrib import admin

from .models import Project, Tag, Issue, Status, File


admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Status)
admin.site.register(File)

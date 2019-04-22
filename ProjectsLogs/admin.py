from django.contrib import admin

# Register your models here.
from .models import Project , Version, Change, Comment, Added, Removed, Coder, WebTechnology
admin.site.register(Project)
admin.site.register(Version)
admin.site.register(Change)
admin.site.register(Added)
admin.site.register(Removed)
admin.site.register(Comment)
admin.site.register(Coder)
admin.site.register(WebTechnology)
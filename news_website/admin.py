from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.Comment)
admin.site.register(models.Profile)
admin.site.register(models.NewsType)


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "publish", "id", "author", )
    search_fields = ("title", "body", )
    prepopulated_fields = {"slug": ("title", )}
    ordering = ("author", "title", )

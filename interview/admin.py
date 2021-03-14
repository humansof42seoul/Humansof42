from django.contrib import admin
from .models import Interview, Comment


# class PhotoInline(admin.TabularInline):
#     model = Photo
#
#
# class InterviewAdmin(admin.ModelAdmin):
#     inlines = [PhotoInline, ]


admin.site.register(Interview)
admin.site.register(Comment)
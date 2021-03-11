from django.contrib import admin

from main.models import CodeImage, Problem, Reply, Comment


class ImageInline(admin.TabularInline):
    model = CodeImage
    max_num = 7
    min_num = 1


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ]


admin.site.register(Reply)
admin.site.register(Comment)

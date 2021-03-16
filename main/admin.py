from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from main.models import CodeImage, Problem, Reply, Comment


class ProblemAdminForm(forms.ModelForm):
    description_ru = forms.CharField(widget=CKEditorWidget())
    description_ky = forms.CharField(widget=CKEditorWidget())
    description_en = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Problem
        fields = '__all__'


class ImageInline(admin.TabularInline):
    model = CodeImage
    max_num = 7
    min_num = 1


@admin.register(Problem)
class ProblemAdmin(TranslationAdmin):
    form = ProblemAdminForm
    inlines = [ImageInline, ]
    list_filter = ('created', 'updated')
    list_display = ('title', )
    # search_fields = ('title', 'description')


admin.site.register(Reply)
admin.site.register(Comment)

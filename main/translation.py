from modeltranslation.translator import translator, TranslationOptions
from .models import Problem


class ProblemTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Problem, ProblemTranslationOptions)

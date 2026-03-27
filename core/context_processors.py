# core/context_processors.py
from django.conf import settings

def global_context(request):
    return {
        'APP_NAME':       settings.APP_NAME,
        'APP_VERSION':    settings.APP_VERSION,
        'FACULTY_NAME':   settings.FACULTY_NAME,
        'UNIVERSITY_NAME':settings.UNIVERSITY_NAME,
    }

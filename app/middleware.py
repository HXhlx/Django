import logging
from django.conf import settings
from django.utils import translation

logger = logging.getLogger('i18n_debug')

class I18nDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.GET.get('lang')
        if lang and lang in [l[0] for l in settings.LANGUAGES]:
            translation.activate(lang)
            request.session[settings.LANGUAGE_COOKIE_NAME] = lang
        
        response = self.get_response(request)
        
        if lang and lang in [l[0] for l in settings.LANGUAGES]:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        
        return response

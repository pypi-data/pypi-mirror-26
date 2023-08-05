import sys
import os.path
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings as django_settings


class DjangoLoggingSettings(object):
    def __init__(self):
        user_settings = getattr(django_settings, 'DJANGO_LOGGING', None)
        self.__settings = dict(
            DEBUG=django_settings.DEBUG,
            CONSOLE_LOG=True,
            SQL_LOG=True,
            LOG_LEVEL='debug' if django_settings.DEBUG else 'info',
            INFO=False,
            DISABLE_EXISTING_LOGGERS=True,
            IGNORED_PATHS=['/admin', '/static', '/favicon.ico'],
            RESPONSE_FIELDS=('status', 'reason', 'charset', 'headers', 'content'),
            CONTENT_JSON_ONLY=True,
            CONTENT_TYPES=None,
            ENCODING='ascii',
            ROTATE_MB=100,
            ROTATE_COUNT=10,
            INDENT_CONSOLE_LOG=2,
            ELASTICSEARCH_ENABLED=False,
            ELASTICSEARCH_SSL=False,
            ELASTICSEARCH_HOSTS=["localhost"],
            ELASTICSEARCH_INDEX="django-logging-json",
            ELASTICSEARCH_AUTH=None
        )

        try:
            self.__settings['LOG_PATH'] = os.path.join(django_settings.BASE_DIR, 'logs')
        except AttributeError:
            raise ImproperlyConfigured('settings.BASE_DIR is note defined. Please define settings.BASE_DIR or override '
                                       'django_logging.LOG_PATH')
        try:
            self.__settings.update(user_settings)
        except TypeError:
            pass

        if self.CONTENT_JSON_ONLY:
            self.__settings['CONTENT_TYPES'] = self.CONTENT_TYPES or []
            self.__settings['CONTENT_TYPES'].append('application/json')


    def __getattr__(self, name):
        return self.__settings.get(name)
            

sys.modules[__name__] = DjangoLoggingSettings()

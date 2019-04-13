from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class PluginApp(AppConfig):
    name = 'pretalx_pages'
    verbose_name = 'Static pages for pretalx'

    class PretalxPluginMeta:
        name = ugettext_lazy('Static pages for pretalx')
        author = 'Tobias Kunze'
        description = ugettext_lazy("Static pages for pretalx, e.g. information, venue listings, a code of conduct, etc.")
        visible = True
        version = '0.0.0'

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'pretalx_pages.PluginApp'

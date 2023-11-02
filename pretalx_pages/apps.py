from django.apps import AppConfig
from django.utils.translation import gettext_lazy

from pretalx_pages import __version__


class PluginApp(AppConfig):
    name = "pretalx_pages"
    verbose_name = "Pages"

    class PretalxPluginMeta:
        name = gettext_lazy("Pages")
        author = "Tobias Kunze"
        description = gettext_lazy(
            "Add static pages to your event site, for example Terms of Service, venue listings, a code of conduct, etc."
        )
        visible = True
        version = __version__
        category = "FEATURE"

    def ready(self):
        from . import signals  # NOQA

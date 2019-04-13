from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FacebookApp(AppConfig):
    name = 'pretalx_pages'
    verbose_name = _("Static pages")

    def ready(self):
        from . import signals

    class PretalxPluginMeta:
        name = _("StaticPages")
        author = _("Moshe Nahmias")
        version = '0.1.0'
        visible = True
        restricted = False
        description = _("This plugin allows you to have static pages in "
                        "pretalx.")


default_app_config = 'pretalx_pages.StaticPages'

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from i18nfield.fields import I18nCharField, I18nTextField
from pretalx.common.mixins.models import LogMixin
from pretalx.common.phrases import phrases
from pretalx.event.models import Event


class Page(LogMixin, models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="pages")
    slug = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name=_("URL to static page"),
        validators=[
            RegexValidator(
                regex="^[a-zA-Z0-9][a-zA-Z0-9.-]+$",
                message=_(
                    "The slug may only contain letters, numbers, dots and dashes."
                ),
            )
        ],
        help_text=_(
            "This will be used to generate the URL of the page. Please only use latin letters, "
            "numbers, dots and dashes. You cannot change this afterwards."
        ),
    )
    position = models.IntegerField(default=0)
    title = I18nCharField(verbose_name=_("Page title"))
    text = I18nTextField(
        verbose_name=_("Page content"), help_text=phrases.base.use_markdown
    )
    link_in_footer = models.BooleanField(
        default=False, verbose_name=_("Show link in the event footer")
    )

    class Meta:
        ordering = ["position", "title"]

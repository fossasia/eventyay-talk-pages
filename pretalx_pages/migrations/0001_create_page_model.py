# Generated by Django 3.0.3 on 2020-03-01 21:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import i18nfield.fields
import pretalx.common.mixins.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("event", "0022_auto_20200124_1213"),
    ]

    operations = [
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        db_index=True,
                        max_length=150,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="The slug may only contain letters, numbers, dots and dashes.",
                                regex="^[a-zA-Z0-9.-]+$",
                            )
                        ],
                    ),
                ),
                ("position", models.IntegerField(default=0)),
                ("title", i18nfield.fields.I18nCharField()),
                ("text", i18nfield.fields.I18nTextField()),
                ("link_in_footer", models.BooleanField(default=False)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pages",
                        to="event.Event",
                    ),
                ),
            ],
            options={"ordering": ["position", "title"],},
            bases=(pretalx.common.mixins.models.LogMixin, models.Model),
        ),
    ]

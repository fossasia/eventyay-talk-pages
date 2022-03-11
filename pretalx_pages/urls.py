from django.urls import re_path
from pretalx.event.models.event import SLUG_CHARS

from . import views

urlpatterns = [
    re_path(
        rf"^orga/event/(?P<event>[{SLUG_CHARS}]+)/pages/$",
        views.PageList.as_view(),
        name="index",
    ),
    re_path(
        rf"^orga/event/(?P<event>[{SLUG_CHARS}]+)/pages/create$",
        views.PageCreate.as_view(),
        name="create",
    ),
    re_path(
        rf"^orga/event/(?P<event>[{SLUG_CHARS}]+)/pages/(?P<page>[{SLUG_CHARS}]+)/$",
        views.PageUpdate.as_view(),
        name="edit",
    ),
    re_path(
        rf"^orga/event/(?P<event>[{SLUG_CHARS}]+)/pages/(?P<page>[{SLUG_CHARS}]+)/delete$",
        views.PageDelete.as_view(),
        name="delete",
    ),
    re_path(
        rf"^orga/event/(?P<event>[{SLUG_CHARS}]+)/pages/(?P<page>[{SLUG_CHARS}]+)/up$",
        views.page_move_up,
        name="up",
    ),
    re_path(
        rf"^orga/event/(?P<event>[{SLUG_CHARS}]+)/pages/(?P<page>[{SLUG_CHARS}]+)/down$",
        views.page_move_down,
        name="down",
    ),
    re_path(
        rf"^(?P<event>[{SLUG_CHARS}]+)/page/(?P<slug>[^/]+)/$",
        views.ShowPageView.as_view(),
        name="show",
    ),
]

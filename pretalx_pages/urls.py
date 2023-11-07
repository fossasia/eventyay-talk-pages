from django.urls import re_path
from pretalx.event.models.event import SLUG_REGEX

from . import views

urlpatterns = [
    re_path(
        rf"^orga/event/(?P<event>{SLUG_REGEX})/pages/$",
        views.PageList.as_view(),
        name="index",
    ),
    re_path(
        rf"^orga/event/(?P<event>{SLUG_REGEX})/pages/create$",
        views.PageCreate.as_view(),
        name="create",
    ),
    re_path(
        rf"^orga/event/(?P<event>{SLUG_REGEX})/pages/(?P<page>{SLUG_REGEX})/$",
        views.PageUpdate.as_view(),
        name="edit",
    ),
    re_path(
        rf"^orga/event/(?P<event>{SLUG_REGEX})/pages/(?P<page>{SLUG_REGEX})/delete$",
        views.PageDelete.as_view(),
        name="delete",
    ),
    re_path(
        rf"^orga/event/(?P<event>{SLUG_REGEX})/pages/(?P<page>{SLUG_REGEX})/up$",
        views.page_move_up,
        name="up",
    ),
    re_path(
        rf"^orga/event/(?P<event>{SLUG_REGEX})/pages/(?P<page>{SLUG_REGEX})/down$",
        views.page_move_down,
        name="down",
    ),
    re_path(
        rf"^(?P<event>{SLUG_REGEX})/page/(?P<slug>[^/]+)/$",
        views.ShowPageView.as_view(),
        name="show",
    ),
]

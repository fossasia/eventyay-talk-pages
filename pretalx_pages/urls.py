from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^orga/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/pages/$',
        views.PageList.as_view(),
        name='index'),
    url(r'^orga/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/pages/create$',
        views.PageCreate.as_view(),
        name='create'),
    url(r'^orga/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/pages/(?P<page>\d+)/$',
        views.PageUpdate.as_view(),
        name='edit'),
    url(r'^orga/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/pages/(?P<page>\d+)/delete$',
        views.PageDelete.as_view(),
        name='delete'),
    url(r'^orga/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/pages/(?P<page>\d+)/up$',
        views.page_move_up,
        name='up'),
    url(r'^orga/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/pages/(?P<page>\d+)/down$',
        views.page_move_down,
        name='down'),
]

event_patterns = [
    url(r'^page/(?P<slug>[^/]+)/$', views.ShowPageView.as_view(), name='show'),
]
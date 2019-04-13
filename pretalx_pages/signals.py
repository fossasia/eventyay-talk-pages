# Register your receivers here
from django.dispatch import receiver
from django.template.loader import get_template
from django.urls import resolve, reverse
from django.utils.translation import ugettext_lazy as _, get_language

# from pretix.base.signals import logentry_display, event_copy_data
# from pretix.control.signals import html_head, nav_event
# from pretix.multidomain.urlreverse import eventreverse
# from pretix.presale.signals import (
#     footer_link, front_page_bottom, html_head as html_head_presale, checkout_confirm_messages
# )
from pretalx.cfp.signals import footer_link
from pretalx.common.signals import EventPluginSignal
from pretalx.event.models import Event
from pretalx.orga.signals import nav_event

from .models import Page


front_page_bottom = EventPluginSignal(
    providing_args=[]
)


@receiver(nav_event, dispatch_uid="pages_nav")
def control_nav_pages(sender, request=None, **kwargs):
    print('in control nav pages')
    if not request.user.has_event_permission(request.organizer, request.event, 'can_change_event_settings',
                                             request=request):
        return []
    url = resolve(request.path_info)
    return [
        {
            'label': _('Pages'),
            'url': reverse('plugins:pretalx_pages:index', kwargs={
                'event': request.event.slug,
                'organizer': request.event.organizer.slug,
            }),
            'active': (url.namespace == 'plugins:pretalx_pages'),
            'icon': 'file-text',
        }
    ]


# @receiver(signal=event_copy_data, dispatch_uid="pages_copy_data")
# def event_copy_data_receiver(sender, other, **kwargs):
#     for p in Page.objects.filter(event=other):
#         p.pk = None
#         p.event = sender
#         p.save()


# @receiver(signal=logentry_display, dispatch_uid="pages_logentry_display")
# def pretalxcontrol_logentry_display(sender, logentry, **kwargs):
#     event_type = logentry.action_type
#     plains = {
#         'pretalx_pages.page.added': _('The page has been created.'),
#         'pretalx_pages.page.changed': _('The page has been modified.'),
#         'pretalx_pages.page.deleted': _('The page has been deleted.'),
#     }
#
#     if event_type in plains:
#         return plains[event_type]


@receiver(footer_link, dispatch_uid="pages_footer_links")
def footer_link_pages(sender, request=None, **kwargs):
    print('in footer links pages')
    return [
            {
                'label': p.title,
                'url': reverse(sender, 'plugins:pretalx_pages:show', kwargs={
                    'slug': p.slug
                })
            } for p in Page.objects.filter(event=sender, link_in_footer=True)
        ]


@receiver(signal=front_page_bottom, dispatch_uid="pages_frontpage_links")
def pretalx_front_page_bottom(sender, **kwargs):
    print('in front page bottom')
    pages = list(Page.objects.filter(event=sender, link_on_frontpage=True))
    if pages:
        template = get_template('pretalx_pages/front_page.html')
        cached = template.render({
            'event': sender,
            'pages': pages
        })
    else:
        cached = ""

    return cached


@receiver(nav_event, dispatch_uid="pages_html_head")
def html_head_control(sender, request=None, **kwargs):
    print('html head control')
    return [
            {
                'label': p.title,
                'url': reverse(sender, 'plugins:pretalx_pages:show', kwargs={
                    'slug': p.slug
                })
            } for p in Page.objects.filter(event=sender, link_in_footer=True)
        ]
    # url = resolve(request.path_info)
    # if url.namespace == 'plugins:pretalx_pages':
    #
    #     template = get_template('pretalx_pages/control_head.html')
    #     return template.render({})
    # else:
    #     return ""


# TODO: check if relevant for pretalx use case
# @receiver(html_head_presale, dispatch_uid="pages_html_head_presale")
# def html_head_presale(sender, request=None, **kwargs):
#     url = resolve(request.path_info)
#     if url.namespace == 'plugins:pretalx_pages':
#         template = get_template('pretalx_pages/presale_head.html')
#         return template.render({})
#     else:
#         return ""


# @receiver(checkout_confirm_messages, dispatch_uid="pages_confirm_messages")
# def confirm_messages(sender, *args, **kwargs):
#     cached = sender.cache.get('pages_confirm_messages_' + get_language())
#     if cached is None:
#         pages = list(Page.objects.filter(event=sender, require_confirmation=True))
#         if pages:
#             cached = {
#                 'pages': _('I have read and agree with the content of the following pages: {plist}').format(
#                     plist=', '.join([
#                         '<a href="{url}" target="_blank">{title}</a>'.format(
#                             title=str(p.title),
#                             url=eventreverse(sender, 'plugins:pretalx_pages:show', kwargs={
#                                 'slug': p.slug
#                             })
#                         ) for p in pages
#                     ])
#                 )
#             }
#         else:
#             cached = {}
#         sender.cache.set('pages_confirm_messages_' + get_language(), cached)
#     return cached

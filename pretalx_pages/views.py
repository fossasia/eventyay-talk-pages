import bleach
from django import forms
from django.contrib import messages
from django.db import transaction
from django.db.models import Max
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    CreateView, DeleteView, ListView, TemplateView, UpdateView,
)
from i18nfield.forms import I18nModelForm

from .models import Page


class PageList(ListView):
    model = Page
    context_object_name = 'pages'
    paginate_by = 20
    template_name = 'pretalx_pages/index.html'
    permission = 'can_change_event_settings'

    def get_queryset(self):
        return Page.objects.filter(event=self.request.event)


def page_move(request, page, up=True):
    """
    This is a helper function to avoid duplicating code in page_move_up and
    page_move_down. It takes a page and a direction and then tries to bring
    all pages for this event in a new order.
    """
    try:
        page = request.event.page_set.get(
            id=page
        )
    except Page.DoesNotExist:
        raise Http404(_("The requested page does not exist."))
    pages = list(request.event.page_set.order_by("position", "title"))

    index = pages.index(page)
    print(index, up)
    if index != 0 and up:
        pages[index - 1], pages[index] = pages[index], pages[index - 1]
    elif index != len(pages) - 1 and not up:
        pages[index + 1], pages[index] = pages[index], pages[index + 1]

    for i, p in enumerate(pages):
        if p.position != i:
            p.position = i
            p.save()

    request.event.cache.clear()
    messages.success(request, _('The order of pages has been updated.'))


def page_move_up(request, organizer, event, page):
    page_move(request, page, up=True)
    return redirect('plugins:pretalx_pages:index',
                    organizer=request.event.organizer.slug,
                    event=request.event.slug)


def page_move_down(request, organizer, event, page):
    page_move(request, page, up=False)
    return redirect('plugins:pretalx_pages:index',
                    organizer=request.event.organizer.slug,
                    event=request.event.slug)


class PageForm(I18nModelForm):

    def __init__(self, *args, **kwargs):
        self.event = kwargs.get('event')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Page
        fields = (
            'title', 'slug', 'text', 'link_in_footer', 'link_on_frontpage', 'require_confirmation'
        )

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Page.objects.filter(slug=slug, event=self.event).exists():
            raise forms.ValidationError(
                _('You already have a page on that URL.'),
                code='duplicate_slug',
            )
        return slug


class PageEditForm(PageForm):
    slug = forms.CharField(label=_('URL form'), disabled=True)

    def clean_slug(self):
        return self.instance.slug


class PageDetailMixin:
    def get_object(self, queryset=None) -> Page:
        try:
            return Page.objects.get(
                event=self.request.event,
                id=self.kwargs['page']
            )
        except Page.DoesNotExist:
            raise Http404(_("The requested page does not exist."))

    def get_success_url(self) -> str:
        return reverse('plugins:pretalx_pages:index', kwargs={
            'organizer': self.request.event.organizer.slug,
            'event': self.request.event.slug,
        })


class PageDelete(PageDetailMixin, DeleteView):
    model = Page
    form_class = PageForm
    template_name = 'pretalx_pages/delete.html'
    context_object_name = 'page'
    permission = 'can_change_event_settings'

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.log_action('pretalx_pages.page.deleted', user=self.request.user)
        self.object.delete()
        messages.success(request, _('The selected page has been deleted.'))
        self.request.event.cache.clear()
        return HttpResponseRedirect(self.get_success_url())


class PageEditorMixin:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['event'] = self.request.event
        return kwargs


class PageUpdate(PageDetailMixin, PageEditorMixin, UpdateView):
    model = Page
    form_class = PageEditForm
    template_name = 'pretalx_pages/form.html'
    context_object_name = 'page'
    permission = 'can_change_event_settings'

    def get_success_url(self) -> str:
        return reverse('plugins:pretalx_pages:edit', kwargs={
            'organizer': self.request.event.organizer.slug,
            'event': self.request.event.slug,
            'page': self.object.pk
        })

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['locales'] = []
        for lng in self.request.event.settings.locales:
            dataline = (
                self.object.text.data[lng]
                if self.object.text is not None and (
                    isinstance(self.object.text.data, dict)
                ) and lng in self.object.text.data
                else ""
            )
            ctx['locales'].append((lng, dataline))
        return ctx

    @transaction.atomic
    def form_valid(self, form):
        messages.success(self.request, _('Your changes have been saved.'))
        if form.has_changed():
            self.object.log_action(
                'pretalx_pages.page.changed', user=self.request.user, data={
                    k: form.cleaned_data.get(k) for k in form.changed_data
                }
            )
        self.request.event.cache.clear()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('We could not save your changes. See below for details.'))
        return super().form_invalid(form)


class PageCreate(PageEditorMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = 'pretalx_pages/form.html'
    permission = 'can_change_event_settings'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['locales'] = [
            (l, "")
            for l in self.request.event.settings.locales
        ]
        return ctx

    def get_success_url(self) -> str:
        return reverse('plugins:pretalx_pages:index', kwargs={
            'organizer': self.request.event.organizer.slug,
            'event': self.request.event.slug,
        })

    @transaction.atomic
    def form_valid(self, form):
        form.instance.event = self.request.event
        form.instance.event = self.request.event
        form.instance.position = (self.request.event.page_set.aggregate(p=Max('position'))['p'] or 0) + 1
        messages.success(self.request, _('The new page has been created.'))
        ret = super().form_valid(form)
        form.instance.log_action('pretalx_pages.page.added', data=dict(form.cleaned_data),
                                 user=self.request.user)
        self.request.event.cache.clear()
        return ret

    def form_invalid(self, form):
        messages.error(self.request, _('We could not save your changes. See below for details.'))
        return super().form_invalid(form)


class ShowPageView(TemplateView):
    template_name = 'pretalx_pages/show.html'

    def get_page(self):
        try:
            return Page.objects.get(
                event=self.request.event,
                slug=self.kwargs['slug']
            )
        except Page.DoesNotExist:
            raise Http404(_("The requested page does not exist."))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        page = self.get_page()
        ctx['page'] = page

        attributes = dict(bleach.ALLOWED_ATTRIBUTES)
        attributes['a'] = ['href', 'title', 'target']
        attributes['p'] = ['class']
        attributes['li'] = ['class']

        ctx['content'] = bleach.clean(str(page.text), tags=bleach.ALLOWED_TAGS + [
            'p',
            'br',
            's',
            'sup',
            'sub',
            'u',
            'h3',
            'h4',
            'h5',
            'h6'
        ], attributes=attributes)
        return ctx
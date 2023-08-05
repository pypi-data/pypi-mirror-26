# -*- coding: utf-8 -*-
""" Popupcrud views """

from functools import update_wrapper
from collections import OrderedDict

from django import forms
from django.conf import settings
from django.conf.urls import include, url
from django.core.exceptions import ImproperlyConfigured, FieldDoesNotExist
from django.shortcuts import render_to_response
from django.views import generic
from django.http import JsonResponse
from django.template import loader
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.utils.decorators import classonlymethod
from django.utils.translation import ugettext_lazy as _, ugettext, override
from django.utils.http import urlencode
from django.utils import six

#from django.contrib.admin import ModelAdmin


from pure_pagination import PaginationMixin

from .widgets import RelatedFieldPopupFormWidget


POPUPCRUD_DEFAULTS = {
    'base_template': 'base.html',

    'page_title_context_variable': 'page_title',

    'paginate_by': 10,
}
"""django-popupcrud global settings are specified as the dict variable
``POPUPCRUD`` in settings.py.

``POPUPCRUD`` currently supports the following settings with their
default values:

    - ``base_template``: The prjoject base template from which all popupcrud
      templates should be derived.

      Defaults to ``base.html``.

    - ``page_title_context_variable``: Name of the context variable whose value
      will be set as the title for the CRUD list view page. This title is
      specified as the value for the class attribute ``ViewSet.page_title`` or
      as the return value of ``ViewSet.get_page_title()``.

      Defaults to ``page_title``.

    - ``paginate_by``: Default number of rows per page for queryset pagination.
      This is the same as ListView.paginate_by.

      Defaults to 10.
"""

# build effective settings by merging any user settings with defaults
POPUPCRUD = POPUPCRUD_DEFAULTS.copy()
POPUPCRUD.update(getattr(settings, 'POPUPCRUD', {}))

ALL_VAR = 'all'
ORDER_VAR = 'o'
ORDER_TYPE_VAR = 'ot'
PAGE_VAR = 'p'
SEARCH_VAR = 'q'
ERROR_FLAG = 'e'

IGNORED_PARAMS = (
    ALL_VAR, ORDER_VAR, ORDER_TYPE_VAR, SEARCH_VAR)

class AjaxObjectFormMixin(object):
    """
    Mixin facilitates single object create/edit functions to be performed
    through an AJAX request.

    Views that provide the feature of creating/editing model objects
    via AJAX requests should derive from this class.

    So if CRUD for a model wants to allow creation of its objects via a popup,
    its CreateView should include this mixin in its derivation chain. Such a
    view an also support its objects being created from the view for another
    model which has a ForeignKey into it and wants to provide 'inline-creation'
    of releated objects from a popup without leaving the context of the model
    object view being created/edited.
    """
    def get_ajax_response(self):
        return JsonResponse({
            'name': str(self.object), # object representation
            'pk': self.object.pk          # object id
        })

    # following two methods are applicable only to Create/Edit views
    def get_form_class(self):
        if getattr(self._viewset, 'form_class', None):
            return self._viewset.form_class
        return super(AjaxObjectFormMixin, self).get_form_class()

    def get_form(self, form_class=None):
        form = super(AjaxObjectFormMixin, self).get_form(form_class)
        if not getattr(self._viewset, 'form_class', None):
            self._init_related_fields(form)
        return form

    def _init_related_fields(self, form):
        related_popups  = getattr(self._viewset, 'related_object_popups', {})
        for fname in related_popups:
            if fname in form.fields:
                field = form.fields[fname]
                if isinstance(form.fields[fname], forms.ModelChoiceField):
                    form.fields[fname].widget = RelatedFieldPopupFormWidget(
                        widget=forms.Select(choices=form.fields[fname].choices),
                        new_url=related_popups[fname])

    def form_valid(self, form): # pylint: disable=missing-docstring
        retval = super(AjaxObjectFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            return self.get_ajax_response()
        return retval

    def handle_no_permission(self):
        if self.request.is_ajax():
            return render_to_response('popupcrud/403.html')
        super(AjaxObjectFormMixin, self).handle_no_permission()


class AttributeThunk(object):
    """
    Class thunks various attributes expected by Django generic CRUD views as
    properties of the parent viewset class instance. This allows us to
    normalize all CRUD view attributes as ViewSet properties and/or methods.
    """
    def __init__(self, viewset, *args, **kwargs):
        self._viewset = viewset()   # Sat 9/9, changed to store Viewset object
                                    # instead of viewset class
        self._viewset.view = self   # allow viewset methods to access view
        super(AttributeThunk, self).__init__(*args, **kwargs)

    @property
    def model(self):
        return self._viewset.model

    @property
    def fields(self):
        return self._viewset.fields

    def get_success_url(self):
        return self._viewset.list_url

    def get_context_data(self, **kwargs):
        kwargs['base_template'] = POPUPCRUD['base_template']
        title_cv = POPUPCRUD['page_title_context_variable']
        kwargs[title_cv] = self._viewset.get_page_title()
        kwargs['viewset'] = self._viewset
        return super(AttributeThunk, self).get_context_data(**kwargs)

    @property
    def login_url(self):
        # If view specific attribute is set in PopupCrudViewSet, return it.
        # Otherwise, return the ViewSet global 'login_url' attr value.
        return getattr(self._viewset,
                       "%s_login_url" % self._get_view_code(),
                       self._viewset.login_url)

    @property
    def raise_exception(self):
        # If view specific attribute is set in PopupCrudViewSet, return it.
        # Otherwise, return the ViewSet global 'raise_exception' attr value.
        return getattr(self._viewset,
                       "%s_raise_exception" % self._get_view_code(),
                       self._viewset.raise_exception)

    def get_permission_required(self):
        return self._viewset.get_permission_required(self._get_view_code())

    def _get_view_code(self):
        """ Returns the short code for this ViewSet view """
        codes = {
            'ListView': 'list',
            'DetailView': 'detail',
            'CreateView': 'create',
            'UpdateView': 'update',
            'DeleteView': 'delete'
        }
        return codes[self.__class__.__name__]


class ListView(AttributeThunk, PaginationMixin, PermissionRequiredMixin,
               generic.ListView):
    """ Model list view """

    def __init__(self, viewset_cls, *args, **kwargs):
        super(ListView, self).__init__(viewset_cls, *args, **kwargs)
        request = kwargs['request']
        self.params = dict(request.GET.items())
        self.query = request.GET.get(SEARCH_VAR, '')
        self.lookup_opts = self.model._meta

    @property
    def media(self):
        popups = self._viewset.popups
        # don't load popupcrud.js if all crud views are set to 'legacy'
        popupcrud_media = forms.Media(
            css={'all': ('popupcrud/css/popupcrud.css',)},
            js=('popupcrud/js/popupcrud.js',))

        # Can't we load media of forms created using modelform_factory()?
        # Need to investigate.
        if self._viewset.form_class:
            popupcrud_media += self._viewset.form_class().media
        return popupcrud_media

    def get_paginate_by(self, queryset):
        return self._viewset.get_paginate_by()

    def get_queryset(self):
        qs = super(ListView, self).get_queryset()

        # Apply any filters

        # Set ordering.
        ordering = self._get_ordering(self.request, qs)
        qs = qs.order_by(*ordering)

        # Apply search results

        return qs

    def get_template_names(self):
        templates = super(ListView, self).get_template_names()

        # if the viewset customized listview template, make sure that is
        # looked for first by putting its name in the front of the list
        if getattr(self._viewset, 'list_template', None):
            templates.insert(0, self._viewset.list_template)

        # make the default template of lower priority than the one
        # determined by default -- <model>_list.html
        templates.append("popupcrud/list.html")
        return templates

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['model_options'] = self._viewset.model._meta
        context['new_button_text'] = ugettext("New {0}").format(
            self._viewset.model._meta.verbose_name)
        context['new_url'] = self._viewset.get_new_url()
        context['new_item_dialog_title'] = ugettext("New {0}").format(
            self.model._meta.verbose_name)
        context['edit_item_dialog_title'] = ugettext("Edit {0}").format(
            self.model._meta.verbose_name)
        context['legacy_crud'] = self._viewset.legacy_crud
        return context

    def _get_default_ordering(self):
        ordering = []
        if self._viewset.ordering:
            ordering = self._viewset.ordering
        elif self.lookup_opts.ordering:
            ordering = self.lookup_opts.ordering
        return ordering

    def get_ordering_field_columns(self):
        """
        Returns an OrderedDict of ordering field column numbers and asc/desc
        """

        # We must cope with more than one column having the same underlying sort
        # field, so we base things on column numbers.
        ordering = self._get_default_ordering()
        ordering_fields = OrderedDict()
        if ORDER_VAR not in self.params:
            # for ordering specified on ModelAdmin or model Meta, we don't know
            # the right column numbers absolutely, because there might be more
            # than one column associated with that ordering, so we guess.
            for field in ordering:
                if field.startswith('-'):
                    field = field[1:]
                    order_type = 'desc'
                else:
                    order_type = 'asc'
                for index, attr in enumerate(self.list_display):
                    if self.get_ordering_field(attr) == field:
                        ordering_fields[index] = order_type
                        break
        else:
            for p in self.params[ORDER_VAR].split('.'):
                none, pfx, idx = p.rpartition('-')
                try:
                    idx = int(idx)
                except ValueError:
                    continue  # skip it
                ordering_fields[idx] = 'desc' if pfx == '-' else 'asc'
        return ordering_fields

    def get_ordering_field(self, field_name):
        """
        Returns the proper model field name corresponding to the given
        field_name to use for ordering. field_name may either be the name of a
        proper model field or the name of a method (on the admin or model) or a
        callable with the 'order_field' attribute. Returns None if no
        proper model field name can be matched.
        """
        try:
            field = self.lookup_opts.get_field(field_name)
            return field.name
        except FieldDoesNotExist:
            # See whether field_name is a name of a non-field
            # that allows sorting.
            if callable(field_name):
                attr = field_name
            elif hasattr(self._viewset, field_name):
                attr = getattr(self._viewset, field_name)
            else:
                attr = getattr(self.model, field_name)
            return getattr(attr, 'order_field', None)

    def _get_ordering(self, request, queryset):
        """
        Returns the list of ordering fields for the change list.
        First we check the get_ordering() method in model admin, then we check
        the object's default ordering. Then, any manually-specified ordering
        from the query string overrides anything. Finally, a deterministic
        order is guaranteed by ensuring the primary key is used as the last
        ordering field.
        """
        params = self.params
        ordering = list(self._get_default_ordering())
        if ORDER_VAR in params:
            # Clear ordering and used params
            ordering = []
            order_params = params[ORDER_VAR].split('.')
            for p in order_params:
                try:
                    none, pfx, idx = p.rpartition('-')
                    field_name = self._viewset.list_display[int(idx)]
                    order_field = self.get_ordering_field(field_name)
                    if not order_field:
                        continue  # No 'order_field', skip it
                    # reverse order if order_field has already "-" as prefix
                    if order_field.startswith('-') and pfx == "-":
                        ordering.append(order_field[1:])
                    else:
                        ordering.append(pfx + order_field)
                except (IndexError, ValueError):
                    continue  # Invalid ordering specified, skip it.

        # Add the given query's ordering fields, if any.
        ordering.extend(queryset.query.order_by)

        # Ensure that the primary key is systematically present in the list of
        # ordering fields so we can guarantee a deterministic order across all
        # database backends.
        pk_name = self.lookup_opts.pk.name
        if not (set(ordering) & {'pk', '-pk', pk_name, '-' + pk_name}):
            # The two sets do not intersect, meaning the pk isn't present. So
            # we add it.
            ordering.append('-pk')

        return ordering

    def get_ordering_field_columns(self):
        """
        Returns an OrderedDict of ordering field column numbers and asc/desc
        """

        # We must cope with more than one column having the same underlying sort
        # field, so we base things on column numbers.
        ordering = self._get_default_ordering()
        ordering_fields = OrderedDict()
        if ORDER_VAR not in self.params:
            # for ordering specified on ModelAdmin or model Meta, we don't know
            # the right column numbers absolutely, because there might be more
            # than one column associated with that ordering, so we guess.
            for field in ordering:
                if field.startswith('-'):
                    field = field[1:]
                    order_type = 'desc'
                else:
                    order_type = 'asc'
                for index, attr in enumerate(self._viewset.list_display):
                    if self.get_ordering_field(attr) == field:
                        ordering_fields[index] = order_type
                        break
        else:
            for p in self.params[ORDER_VAR].split('.'):
                none, pfx, idx = p.rpartition('-')
                try:
                    idx = int(idx)
                except ValueError:
                    continue  # skip it
                ordering_fields[idx] = 'desc' if pfx == '-' else 'asc'
        return ordering_fields

    def get_query_string(self, new_params=None, remove=None):
        if new_params is None:
            new_params = {}
        if remove is None:
            remove = []
        p = self.params.copy()
        for r in remove:
            for k in list(p):
                if k.startswith(r):
                    del p[k]
        for k, v in new_params.items():
            if v is None:
                if k in p:
                    del p[k]
            else:
                p[k] = v
        return '?%s' % urlencode(sorted(p.items()))


class TemplateNameMixin(object):
    """
    Mixin adds the ViewSet attribute, set by 'popupcrud_template_name` view
    attribute value, as one of the templates to the list of templates to be
    looked up for rendering the view.

    And if the incoming request is an AJAX request, it replaces all the template
    filenames with '_inner' such that site common embellishments are removed
    while rendering the view content inside a modal popup. Of course it's assumed
    that the '_inner.html' template is written as a pure template, which doesn't
    derive from the site common base template.
    """
    def get_template_names(self):
        templates = super(TemplateNameMixin, self).get_template_names()

        # if the viewset customized listview template, make sure that is
        # looked for first by putting its name in the front of the list
        template_attr_name = getattr(self, "popupcrud_template_name", None)

        if hasattr(self._viewset, template_attr_name):
            templates.insert(0, getattr(self._viewset, template_attr_name))

        # make the default template of lower priority than the one
        # determined by default -- <model>_list.html
        templates.append(getattr(self, template_attr_name))

        if self.request.is_ajax():
            # If this is an AJAX request, replace all the template names with
            # their <template_name>_inner.html counterparts.
            # These 'inner' templates are expected to be a bare-bones templates,
            # sans the base template's site-common embellishments.
            for index, template in enumerate(templates):
                parts = template.split('.')
                templates[index] = "{0}_inner.{1}".format(parts[0], parts[1])

        return templates


class CreateView(AttributeThunk, TemplateNameMixin, AjaxObjectFormMixin,
                 PermissionRequiredMixin, generic.CreateView):

    popupcrud_template_name = "form_template"
    form_template = "popupcrud/form.html"

    def __init__(self, viewset_cls, *args, **kwargs):
        super(CreateView, self).__init__(viewset_cls, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['pagetitle'] = ugettext("New {0}").format(self._viewset.model._meta.verbose_name)
        kwargs['form_url'] = self._viewset.get_new_url()
        return super(CreateView, self).get_context_data(**kwargs)


class DetailView(AttributeThunk, TemplateNameMixin, PermissionRequiredMixin,
                 generic.DetailView):

    popupcrud_template_name = "detail_template"
    detail_template = "popupcrud/detail.html"

    def __init__(self, viewset_cls, *args, **kwargs):
        super(DetailView, self).__init__(viewset_cls, *args, **kwargs)


class UpdateView(AttributeThunk, TemplateNameMixin, AjaxObjectFormMixin,
                 PermissionRequiredMixin, generic.UpdateView):

    popupcrud_template_name = "form_template"
    form_template = "popupcrud/form.html"

    def __init__(self, viewset_cls, *args, **kwargs):
        super(UpdateView, self).__init__(viewset_cls, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['pagetitle'] = _("Edit {0}").format(self._viewset.model._meta.verbose_name)
        kwargs['form_url'] = self._viewset.get_edit_url(self.object)
        return super(UpdateView, self).get_context_data(**kwargs)


class DeleteView(AttributeThunk, PermissionRequiredMixin, generic.DeleteView):

    template_name = "popupcrud/confirm_delete.html"

    def __init__(self, viewset_cls, *args, **kwargs):
        super(DeleteView, self).__init__(viewset_cls, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['pagetitle'] = _("Delete {0}").format(self._viewset.model._meta.verbose_name)
        kwargs['model_options'] = self._viewset.model._meta
        return super(DeleteView, self).get_context_data(**kwargs)

    def handle_no_permission(self):
        """
        Slightly different form of handling no_permission from Create/Update
        views. Delete ajax request expects a JSON response to its AJAX request
        and therefore we render the 403 template and return the rendered context
        as error message text.
        """
        if self.request.is_ajax():
            temp = loader.get_template("popupcrud/403.html")
            return JsonResponse({
                'result': False,
                'message': temp.render({}, self.request)
            })
        super(DeleteView, self).handle_no_permission()

    def delete(self, request, *args, **kwargs):
        """ Override to return JSON success response for AJAX requests """
        retval = super(DeleteView, self).delete(request, *args, **kwargs)
        if self.request.is_ajax():
            return JsonResponse({
                'result': True,
                'message': ugettext("{0} {1} deleted").format(
                    self.model._meta.verbose_name,
                    str(self.object))
            })
        else:
            messages.info(self.request, _("{0} {1} deleted").format(
                self._viewset.model._meta.verbose_name,
                str(self.object)))
            return retval


class PopupCrudViewSet(object):
    """
    This is the base class from which you derive a class in your project
    for each model that you need to build CRUD views for.
    """

    """
        Optional:

            Class Properties:
                list_template: the template file to use for list view
                create_template: template to use for create new object view
                edit_template: template to use for editing an existing object view
                detail_template: template to use for detail view
                delete_template: template to use for delete view

            Methods:
                get_detail_url: staticmetod. Return the url to the object's

                    detail view. Default implementation in base class returns
                    None, which disables the object detail view.

    3. Connect the five different methods to the url resolver. For example:

        MyModelViewset(PopupCrudViewSet):
            model = MyModel
            ...

        urlpatterns = [
            url(r'mymodel/$', MyModelViewset.list(), name='mymodels-list'),
            url(r'mymodel/new/$', MyModelViewset.create(), name='new-mymodel'),
            url(r'mymodel/(?P<pk>\d+)/$', MyModelViewset.detail(), name='mymodel-detail'),
            url(r'mymodel/(?P<pk>\d+)/edit/$', MyModelViewset.update(), name='edit-mymodel'),
            url(r'mymodel/(?P<pk>\d+)/delete/$', MyModelViewset.delete(), name='delete-mymodel'),
            ]
    """
    _urls = None    # urls cache, so that we don't build it for every request

    #: The model to build CRUD views for. This is a required attribute.
    model = None

    #: URL to the create view for creating a new object. This is a required
    #: attribute.
    new_url = None

    #: Lists the fields to be displayed in the list view columns. This attribute
    #: is modelled after ModelAdmin.list_display and supports model methods as
    #: as ViewSet methods much like ModelAdmin. This is a required attribute.
    #:
    #: So you have four possible values that can be used in list_display:
    #:
    #:  - A field of the model
    #:  - A callable that accepts one parameter for the model instance.
    #:  - A string representing an attribute on ViewSet class.
    #:  - A string representing an attribute on the model
    #:
    #: See ModelAdmin.list_display `documentation
    #: <https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display>`_
    #: for examples.
    #:
    #: A note about ``list_display`` fields with respect to how it differs from
    #: ``ModelAdmin``'s ``list_display``.
    #:
    #: In ``ModelAdmin``, if a field specified in ``list_display`` is not
    #: a database field, it can be set as a sortable field by setting
    #: the method's ``admin_order_field`` attribute to the relevant database
    #: field that can be used as the sort field. In ``PopupCrudViewSet``, this
    #: attribute is named ``order_Field``.
    list_display = ()

    #: A list of names of fields. This is interpreted the same as the Meta.fields
    #: attribute of ModelForm. This is a required attribute.
    fields = ()

    #: The form class to instantiate for Create and Update views. This is optional
    #: and if not specified a ModelForm using the values of fields attribute will
    #: be instantiated. An optional attribute, if specified, overrides fields
    #: attribute value.
    form_class = None

    #: The url where the list view is rooted. This will be used as the success_url
    #: attribute value for the individual CRUD views. This is a required attribute.
    list_url = None

    #: Number of entries per page in list view. Defaults to 10. Setting this
    #: to None will disable pagination. This is an optional attribute.
    paginate_by = POPUPCRUD['paginate_by'] #10 # turn on pagination by default

    #: List of permission names for the list view. Permission names are of the
    #: same format as what is specified in ``permission_required()`` decorator.
    #: Defaults to no permissions, meaning no permission is required.
    list_permission_required = ()

    #: List of permission names for the create view.
    #: Defaults to no permissions, meaning no permission is required.
    create_permission_required = ()

    #: List of permission names for the detail view.
    #: Defaults to no permissions, meaning no permission is required.
    detail_permission_required = ()

    #: List of permission names for the update view.
    #: Defaults to no permissions, meaning no permission is required.
    update_permission_required = ()

    #: List of permission names for the delete view.
    #: Defaults to no permissions, meaning no permission is required.
    delete_permission_required = ()

    #: The template file to use for list view. If not specified, defaults
    #: to the internal template.
    list_template = None

    # #: The template file to use for create view. If not specified, defaults
    # #: to the internal template.
    #create_template: template to use for create new object view
    #edit_template: template to use for editing an existing object view
    #detail_template: template to use for detail view
    #delete_template: template to use for delete view

    #: A table that maps foreign keys to its target model's
    #: ``PopupCrudViewSet.create()`` view url. This would result in the select box
    #: for the foreign key to display a 'New {model}' link at its bottom, which
    #: the user can click to add a new {model} object from another popup. The
    #: newly created {model} object will be added to the select's options and
    #: set as its selected option.
    #:
    #: Defaults to empty dict, meaning creation of target model objects, for the
    #: foreign keys of a model, from a popup is disabled.
    related_object_popups = {}

    #: Page title for the list view page.
    page_title = ''

    ordering = None

    #: Enables legacy CRUD views where each of the Create, Detail, Update &
    #: Delete views are performed from their own dedicated web views like Django
    #: admin (hence the term ``legacy_crud`` :-)).
    #:
    #: This property can accept either a boolean value, which in turn enables/
    #: disables the legacy mode for all the CRUD views or it can accept
    #: a dict of CRUD operation codes and its corresponding legacy mode
    #: specified as boolean value.
    #:
    #: This dict looks like::
    #:
    #:      legacy_crud = {
    #:          'create': False,
    #:          'detail': False,
    #:          'update': False,
    #:          'delete': False
    #:      }
    #:
    #: So by setting ``legacy_crud[detail] = True``, you can enable legacy style
    #: crud for the detail view whereas the rest of the CRUD operations are
    #: performed from a modal popup.
    #:
    #: In other words, ``legacy_crud`` boolean value results in a dict that
    #: consists of ``True`` or ``False`` values for all its keys, as the case
    #: may be.
    #:
    #: This defaults to ``False``, which translates into a dict consisting of
    #: ``False`` values for all its keys.
    legacy_crud = False

    #: Same as ``django.contrib.auth.mixins.AccessMixin`` ``login_url``, but
    #: applicable for all CRUD views.
    login_url = None

    #: Same as ``django.contrib.auth.mixins.AccessMixin`` ``raise_exception``,
    #: but applicable for all CRUD views.
    raise_exception = False

    popup_views = {
        'create': True,
        'detail': True,
        'update': True,
        'delete': True,
    }

    @classonlymethod
    def _generate_view(cls, crud_view_class, **initkwargs):
        """
        A closure that generates the view function by instantiating the view
        class specified in argument 2. This is a generalized function that is
        used by the four CRUD methods (list, create, read, update & delete) to
        generate their individual Django CBV based view instances.

        Returns the thus generated view function which can be used in url()
        function as second argument.

        Code is mostly extracted from django CBV View.as_view(), removing the
        update_wrapper() calls at the end.
        """
        def view(request, *args, **kwargs):
            initkwargs['request'] = request
            view = crud_view_class(cls, **initkwargs)
            if hasattr(view, 'get') and not hasattr(view, 'head'):
                view.head = view.get
            view.request = request
            view.args = args
            view.kwargs = kwargs
            return view.dispatch(request, *args, **kwargs)

        view.view_class = crud_view_class
        view.view_initkwargs = initkwargs

        # take name and docstring from class
        #update_wrapper(view, crud_view_class, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        #update_wrapper(view, crud_view_class.dispatch, assigned=())
        return view

    def __init__(self, *args, **kwargs):
        self.view = None

    @classonlymethod
    def list(cls, **initkwargs):
        """Returns the list view that can be specified as the second argument
        to url() in urls.py.
        """
        return cls._generate_view(ListView, **initkwargs)

    @classonlymethod
    def create(cls, **initkwargs):
        """Returns the create view that can be specified as the second argument
        to url() in urls.py.
        """
        return cls._generate_view(CreateView, **initkwargs)

    @classonlymethod
    def detail(cls, **initkwargs):
        """Returns the create view that can be specified as the second argument
        to url() in urls.py.
        """
        return cls._generate_view(DetailView, **initkwargs)

    @classonlymethod
    def update(cls, **initkwargs):
        """Returns the update view that can be specified as the second argument
        to url() in urls.py.
        """
        return cls._generate_view(UpdateView, **initkwargs)

    @classonlymethod
    def delete(cls, **initkwargs):
        """Returns the delete view that can be specified as the second argument
        to url() in urls.py.
        """
        return cls._generate_view(DeleteView, **initkwargs)

    def get_new_url(self):
        """ Returns the URL to create a new model object. Returning None would
        disable the new object creation feature and will hide the ``New {model}``
        button.

        You may override this to dynamically determine if new object creation
        ought to be allowed. Default implementation returns the value of
        ``ViewSet.new_url``.
        """
        return self.new_url

    def get_detail_url(self, obj):
        """ Override this returning the URL where ``PopupCrudViewSet.detail()``
        is placed in the URL namespace such that ViewSet can generate the
        appropriate href to display item detail in list view.

        When this hyperlink is clicked, a popup containing the
        object's detail will be shown. By default this popup only shows the
        object's string representation. To show additional information in this
        popup, implement ``<object>_detail.html`` in your project, typically in
        the app's template folder. If this file exists, it will be used to
        render the object detail popup. True to Django's ``DetailView``
        convention, you may use the ``{{ object }}`` template variable in the
        template file to access the object and its properties.

        Default implementations returns None, which results in object detail
        popup being disabled.
        """
        return None

    def get_edit_url(self, obj):
        """ Override this returning the URL where PopupCrudViewSet.update() is
        placed in the URL namespace such that ViewSet can generate the
        appropriate href to the item edit hyperlink in list view.

        If None is returned, link to edit the specified item won't be
        shown in the object row.
        """
        return "#"

    def get_delete_url(self, obj):
        """ Override this returning the URL where PopupCrudViewSet.delete() is
        placed in the URL namespace such that ViewSet can generate the
        appropriate href to the item delete hyperlink in list view.

        If None is returned, link to delete the specified item won't be
        shown in the object row.
        """
        return "#"

    def get_obj_name(self, obj):
        """ Return the name of the object that will be displayed in item
        action prompts for confirmation. Defaults to ``str(obj)``, ie., the
        string representation of the object. Override this to provide the user
        with additional object details. The returned string may contain
        embedded HTML tags.

        For example, you might want to display the balance due from a customer
        when confirming user action to delete the customer record.
        """
        return six.text_type(obj)

    def get_permission_required(self, op):
        """
        Return the permission required for the CRUD operation specified in op.
        Default implementation returns the value of one
        ``{list|create|detail|update|delete}_permission_required`` class attributes.
        Overriding this allows you to return dynamically computed permissions.

        :param op: The CRUD operation code. One of
            ``{'list'|'create'|'detail'|'update'|'delete'}``.

        :rtype:
            The ``permission_required`` tuple for the specified operation.
            Determined by looking up the given ``op`` from the table::

                permission_table = {
                    'list': self.list_permission_required,
                    'create': self.create_permission_required,
                    'detail': self.detail_permission_required,
                    'update': self.update_permission_required,
                    'delete': self.delete_permission_required
                }
        """
        permission_table = {
            'list': self.list_permission_required,
            'create': self.create_permission_required,
            'detail': self.detail_permission_required,
            'update': self.update_permission_required,
            'delete': self.delete_permission_required
        }
        return permission_table[op]

    def get_page_title(self):
        #: Returns the page title for the list view. By default returns the
        #: value of class variable ``page_title``.
        return self.page_title if self.page_title else \
                self.model._meta.verbose_name_plural

    def get_paginate_by(self):
        #: Returns the number of items to paginate by, or None for no
        #: pagination. By default this simply returns the value of
        #: ``paginate_by``.
        return self.paginate_by

    @classonlymethod
    def urls(cls, namespace=None, views=('create', 'update', 'delete', 'detail')):
        """
        Returns the CRUD urls for the viewset that can be added to the URLconf.
        The URLs returned can be controlled by the ``views`` parameter which
        is tuple of strings specifying the CRUD operations URLs to be returned.
        This defaults to all the CRUD operations: list, create, read(detail),
        update & delete.

        This method can be seen as a wrapper to calling the individual view
        generator methods, ``list()``, ``detail()``, ``create()``, ``update()``
        & ``delete()``, to register them with the URLconf.

        :param namespace: The namespace under which the CRUD urls are registered.
            Defaults to the value of ``<model>.Meta.verbose_name_plural`` (in
            lowercase).
        :param views: A tuple of strings representing the CRUD views whose URL
            patterns are to be registered. Defaults to ``('create', 'update',
            'delete', 'detail')``, that is all the CRUD operations for the model.

        :rtype:
            A collection of URLs, packaged using ``django.conf.urls.include()``,
            that can be used as argument 2 to ``url()`` (see example below).

        :example:
            The following pattern registers all the CRUD urls
            for model Book (in app ``library``), generated by BooksCrudViewSet::

                urlpatterns += [
                    url(r'^books/', BooksCrudViewSet.urls())
                ]

            This allows us to refer to individual CRUD operation url as::

                reverse("library:books:list")
                reverse("library:books:create")
                reverse("library:books:detail", kwargs={'pk': book.pk})
                reverse("library:books:update", kwargs={'pk': book.pk})
                reverse("library:books:delete", kwargs={'pk': book.pk})

        """
        if not cls._urls:
            if not namespace:
                with override('en'): # force URLs to be in English even when
                                     # default language is set to something else
                    namespace = cls.model._meta.verbose_name_plural.lower()

            # start with only list url, the rest are optional based on views arg
            urls = [url(r'$', cls.list(), name='list')]

            if 'detail' in views:
                urls.insert(0, url(r'^(?P<pk>\d+)/$', cls.detail(), name='detail'))

            if 'delete' in views:
                urls.insert(0, url(r'^(?P<pk>\d+)/delete/$', cls.delete(), name='delete'))

            if 'update' in views:
                urls.insert(0, url(r'^(?P<pk>\d+)/update/$', cls.update(), name='update'))

            if 'create' in views:
                urls.insert(0, url(r'^create/$', cls.create(), name='create'))

            cls._urls = include(urls, namespace)

        return cls._urls

    @property
    def popups(self):
        """
        Provides a normalized dict of crud view types to use for the viewset
        depending on client.legacy_crud setting.

        Computes this dict only one per object as an optimization.
        """
        if not hasattr(self, '_popups'):
            popups_enabled = {
                'detail': True, 'create': True, 'update': True, 'delete': True
            }
            if isinstance(self.legacy_crud, dict):
                _popups = popups_enabled
                for k, v in self.legacy_crud.items():
                    _popups[k] = False if v else True
            else:
                popups_disabled = popups_enabled.copy()
                for k, v in popups_disabled.items():
                    popups_disabled[k] = False
                _popups = popups_disabled if self.legacy_crud else popups_enabled
            self._popups = _popups

        return self._popups

from django.views.generic import UpdateView
from django.views.generic.base import View
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from django.views.generic.edit import FormMixin


class CreateUpdateView(UpdateView):
	def get_object(self, queryset=None):
		self.creating = False
		obj = self.do_get_object(queryset)
		if obj is None:
			self.creating = True
		return obj

	def do_get_object(self, queryset):
		try:
			return super().get_object(queryset)
		except AttributeError:
			return None


class GETFormMixin(FormMixin):
	def get_form_kwargs(self):
		"""Return the keyword arguments for instantiating the form."""
		kwargs = super().get_form_kwargs()

		if self.request.method == "GET" and self.request.GET:
			kwargs.update({
				'data': self.request.GET,
			})
		return kwargs


class BaseSearchView(GETFormMixin, MultipleObjectMixin, View):
	"""
	Base view for searching objects.

	Using this base class requires subclassing to provide a response mixin.
	"""
	def get(self, request, *args, **kwargs):
		self.form = self.get_form()
		self.object_list = self.get_queryset()

		context = self.get_context_data(form=self.form)
		return self.render_to_response(context)


class SearchView(MultipleObjectTemplateResponseMixin, BaseSearchView):
	"""
	View for searching objects, with a response rendered by a template.
	"""
	template_name_suffix = '_search'

from django.urls import reverse
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.utils.translation import gettext as _
from django.db.models import Q

from base.views import CreateUpdateView, SearchView
from .models import Place, Rating, update_place_scores
from .forms import PlaceSearchForm


class PlaceSearchView(SearchView):
	form_class = PlaceSearchForm
	# model = Place
	paginate_by = 6

	def get_queryset(self):
		if self.form.is_valid():
			query = self.form.cleaned_data['q']
			queryset = Place.objects.filter(
				Q(name__icontains=query)
			)
		else:
			queryset = Place.objects.none()
		self.queryset = queryset
		return super().get_queryset()


class PlaceView(DetailView):
	model = Place


class RatingsView(DetailView):
	model = Place
	template_name = 'places/ratings.html'


class RateView(LoginRequiredMixin, CreateUpdateView):
	model = Rating
	fields = ['sound_intensity', 'light_intensity', 'smell_intensity', 'spaciousness']
	template_name = 'places/rate.html'

	def do_get_object(self, queryset):
		user = self.request.user
		if not user.is_authenticated:
			raise Http404(_("No authenticated user."))

		self.place_pk = self.kwargs.get('pk')
		try:
			self.place = Place.objects.get(pk=self.place_pk)
		except (Place.DoesNotExist, Place.MultipleObjectsReturned):
			raise Http404(_("No unique place found matching the query."))

		if queryset is None:
			queryset = self.get_queryset()
		queryset = queryset.filter(user=user, place=self.place)

		try:
			obj = queryset.get()
		except (queryset.model.DoesNotExist):
			obj = None
		return obj

	def get_context_data(self, **kwargs):
		"""Insert the place into the context dict."""
		kwargs.setdefault('place', self.place)
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		if self.creating:
			form.instance.user = self.request.user
			form.instance.place = self.place
		response = super().form_valid(form)
		update_place_scores(self.place)
		return response

	def get_success_url(self):
		"""Return the URL to redirect to after processing a valid form."""
		return reverse('places:rate', args=(self.place_pk,))

from collections import namedtuple
from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.db.models import Sum, Count
# from address.models import AddressField


minRating = 1
maxRating = 5
ratingValidators = [MinValueValidator(minRating), MaxValueValidator(maxRating)]


class Place(models.Model):
	name = models.TextField(max_length=280)
	address = models.TextField(max_length=280)
	sound_intensity_rating = models.FloatField(validators=ratingValidators, null=True, blank=True)
	light_intensity_rating = models.FloatField(validators=ratingValidators, null=True, blank=True)
	smell_intensity_rating = models.FloatField(validators=ratingValidators, null=True, blank=True)
	spaciousness_rating = models.FloatField(validators=ratingValidators, null=True, blank=True)
	total_rating = models.FloatField(validators=ratingValidators, null=True, blank=True)

	def update_ratings(self, subratings, total_rating):
		for sn in subratings._fields:
			try:
				v = getattr(subratings, sn)
				setattr(self, sn + '_rating', v)
			except AttributeError:
				pass
		self.total_rating = total_rating
		self.save()

	def get_absolute_url(self):
		return reverse('places:place', kwargs={'pk': self.pk})

	def __str__(self):
		return self.name


class Rating(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	place = models.ForeignKey(Place, on_delete=models.CASCADE)
	sound_intensity = models.IntegerField(validators=ratingValidators, null=True, blank=True)
	light_intensity = models.IntegerField(validators=ratingValidators, null=True, blank=True)
	smell_intensity = models.IntegerField(validators=ratingValidators, null=True, blank=True)
	spaciousness = models.IntegerField(validators=ratingValidators, null=True, blank=True)

	@staticmethod
	def get_subratings():
		return namedtuple('Subratings', [
			'sound_intensity',
			'light_intensity',
			'smell_intensity',
			'spaciousness',
		])

	class Meta:
		constraints = [
			UniqueConstraint(fields=['user', 'place'], name='rating_once')
		]


def update_place_scores(place):
	Subratings = Rating.get_subratings()

	scores = place.rating_set.aggregate(
		*([Sum(sn) for sn in Subratings._fields]
		+ [Count(sn) for sn in Subratings._fields])
	)

	scores = {k: (v if v is not None else 0) for k, v in scores.items()}

	total_sum = (scores['sound_intensity__sum'] + scores['light_intensity__sum']
		+ scores['smell_intensity__sum'] + scores['spaciousness__sum'])
	total_count = (scores['sound_intensity__count'] + scores['light_intensity__count']
		+ scores['smell_intensity__count'] + scores['spaciousness__count'])

	def avg(sum, count):
		return sum / count if count != 0 else None

	subratings = Subratings(
		sound_intensity = avg(scores['sound_intensity__sum'], scores['sound_intensity__count']),
		light_intensity = avg(scores['light_intensity__sum'], scores['light_intensity__count']),
		smell_intensity = avg(scores['smell_intensity__sum'], scores['smell_intensity__count']),
		spaciousness = avg(scores['spaciousness__sum'], scores['spaciousness__count']),
	)
	total_rating = avg(total_sum, total_count)
	place.update_ratings(subratings=subratings, total_rating=total_rating)

from django import forms
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit

from .models import Rating


# submit = Submit('', 'Search')
# submit.field_classes = 'btn btn-success'

class PlaceSearchForm(forms.Form):
	# helper = FormHelper()
	# helper.form_show_labels = False
	# helper.add_input(submit)
	# helper.disable_csrf = True
	q = forms.CharField(label='', max_length=80)


# class RatingWidget(forms.NumberInput):
	# template_name = 'places/rating_widget.html'

rating_widget = forms.NumberInput({
	'class': 'rating rating-loading',
	'step': '1',
	'data-theme': 'krajee-svg',
	'data-animate': 'false',
	'data-show-caption': 'false',
	'data-star-titles': 'false',
})

class RatingForm(forms.ModelForm):
	class Meta:
		model = Rating
		fields = ['sound_intensity', 'light_intensity', 'smell_intensity', 'spaciousness']
		widgets = {k: rating_widget for k in fields}

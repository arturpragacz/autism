from django import forms


class PlaceSearchForm(forms.Form):
	q = forms.CharField(label='Search', max_length=50)

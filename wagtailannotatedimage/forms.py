from django import forms


class BaseAnnotationForm(forms.Form):
    annotation_number = forms.IntegerField(max_value=100, min_value=1,
                                           widget=forms.HiddenInput)

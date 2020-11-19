from django import forms


class BaseAnnotationForm(forms.Form):
    prefix = 'annotation'
    annotation_number = forms.IntegerField(max_value=100, min_value=1,
                                           widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(BaseAnnotationForm, self).__init__(*args, auto_id=False, **kwargs)

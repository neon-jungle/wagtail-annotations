import json

from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.admin.edit_handlers import (MultiFieldPanel, FieldPanel,
                                         widget_with_script)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.widgets import AdminImageChooser

from .forms import BaseAnnotationForm


class HiddenJsonInput(forms.HiddenInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value is None or value == '{}':
            value = '{}'
        elif isinstance(value, dict):
            value = json.dumps(value)
        return super(HiddenJsonInput, self).render(name, value, attrs, renderer)

class AnnotatedImagePanel(MultiFieldPanel):
    template = 'annotated_image.html'
    # template = 'wagtailadmin/edit_handlers/multi_field_panel.html'
    js_template = 'annotated_image.js'
    
    def __init__(self, image_field, annotations_field,
                 annotation_form=BaseAnnotationForm(), *args, **kwargs):
        children = (
            ImageChooserPanel(image_field),
            FieldPanel(annotations_field, widget=HiddenJsonInput)
        )
        super().__init__(children=children, *args, **kwargs)
        self.image_field = image_field
        self.annotations_field = annotations_field
        self.annotation_form = annotation_form
    

    def on_form_bound(self):
        super().on_form_bound()
        self.image_field_id = self.children[0].bound_field.auto_id

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        del kwargs['children']
        kwargs.update(
            image_field=self.image_field,
            annotations_field=self.annotations_field,
            annotation_form=self.annotation_form
        )
        return kwargs

    def render(self):
        html = mark_safe(render_to_string(self.template, {
            'panel': self,
            'image_field_id': self.image_field_id,  # Used as js container id
            'image_field': self.children[0],
            'annotations_field': self.children[1],
            'annotation_form': self.annotation_form.as_p(),
            'heading': self.heading,
        }))
        js = self.render_js_init()
        return widget_with_script(html, js)

    def render_js_init(self):
        print('myes')
        return mark_safe(render_to_string(self.js_template, {
            'image_field_id': self.image_field_id,
        }))


class AnnotatedImagePanel2(object):
    def __init__(self, image_field, annotations_field,
                 annotation_form=BaseAnnotationForm(), heading=''):
        self.children = [
            ImageChooserPanel(image_field), FieldPanel(annotations_field)]
        self.heading = heading
        self.annotation_form = annotation_form

    def bind_to(self, model=None, instance=None, request=None, form=None):
        super().bind_to()
        return type(str('_AnnotatedImagePanel'), (BaseAnnotatedImagePanel,), {
            'model': model,
            'children': [child.bind_to(model) for child in self.children],
            'heading': self.heading,
            'annotation_form': self.annotation_form
        })

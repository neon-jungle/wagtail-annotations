import json

from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.wagtailadmin.edit_handlers import (BaseCompositeEditHandler,
                                                FieldPanel, widget_with_script)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.widgets import AdminImageChooser

from .forms import BaseAnnotationForm


class HiddenJsonInput(forms.HiddenInput):
    def render(self, name, value, attrs=None):
        if value is None or value == '{}':
            value = '{}'
        elif isinstance(value, dict):
            value = json.dumps(value)
        return super(HiddenJsonInput, self).render(name, value, attrs)


class BaseAnnotatedImagePanel(BaseCompositeEditHandler):
    template = 'annotated_image.html'
    js_template = 'annotated_image.js'

    @classmethod
    def widget_overrides(cls):
        return {
            cls.children[0].field_name: AdminImageChooser,
            cls.children[1].field_name: HiddenJsonInput}

    def __init__(self, instance=None, form=None):
        super(BaseAnnotatedImagePanel, self).__init__(instance=instance,
                                                      form=form)
        self.image_field = self.children[0]
        self.image_field_id = self.image_field.bound_field.auto_id
        self.annotations_field = self.children[1]

    def render(self):
        html = mark_safe(render_to_string(self.template, {
            'panel': self,
            'image_field_id': self.image_field_id,  # Used as js container id
            'image_field': self.image_field,
            'annotations_field': self.annotations_field,
            'annotation_form': self.annotation_form.as_p(),
            'heading': self.heading,
        }))
        js = self.render_js_init()
        return widget_with_script(html, js)

    def render_js_init(self):
        return mark_safe(render_to_string(self.js_template, {
            'image_field_id': self.image_field_id,
        }))
class AnnotatedImagePanel(object):
    def __init__(self, image_field, annotations_field,
                 annotation_form=BaseAnnotationForm(), heading=''):
        self.children = [
            ImageChooserPanel(image_field), FieldPanel(annotations_field)]
        self.heading = heading
        self.annotation_form = annotation_form

    def bind_to_model(self, model):
        return type(str('_AnnotatedImagePanel'), (BaseAnnotatedImagePanel,), {
            'model': model,
            'children': [child.bind_to_model(model) for child in self.children],
            'heading': self.heading,
            'annotation_form': self.annotation_form
        })

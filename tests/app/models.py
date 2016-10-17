from __future__ import unicode_literals

from django import forms
from django.db import models
from wagtail.wagtailcore.models import Page

from wagtailannotatedimage.edit_handlers import AnnotatedImagePanel
from wagtailannotatedimage.fields import AnnotationsField
from wagtailannotatedimage.forms import BaseAnnotationForm


class AnnotationForm(BaseAnnotationForm):
    text = forms.CharField(widget=forms.TextInput)


class TestPage(Page):
    image = models.ForeignKey('wagtailimages.Image', blank=True, null=True,
                              on_delete=models.SET_NULL, related_name="+")
    annotations = AnnotationsField(blank=True)

    content_panels = Page.content_panels + [
        AnnotatedImagePanel(
            'image', 'annotations',
            annotation_form=AnnotationForm(), heading='Annotated Image'
        )
    ]

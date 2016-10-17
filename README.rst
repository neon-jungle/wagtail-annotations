Wagtail Annotated Image
=======================

Allows users to combine a Wagtail image with custom annotation data. Annotations are entered on the backend by
clicking points on an image, annotation data is then stored with relative x,y coordinates with custom form data.

.. image:: https://giant.gfycat.com/SpeedyHospitableHornet.gif

Requirements
------------

-  Wagtail >= 1.5


Installing
----------

Install using pypi

.. code:: bash

    pip install wagtailannotatedimage

Using
-----

Extend the BaseAnnotationForm to define what data should be stored with annotations.
AnnotationsField stores the annotations data as a Map with id for the annotation being the key.

.. code:: python

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

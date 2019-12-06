Wagtail Annotated Image
=======================

Allows users to combine a Wagtail image with custom annotation data. Annotations are entered in the admin by
clicking points on an image, annotation data is then stored with relative x,y coordinates with custom form data.

.. image:: https://giant.gfycat.com/SpeedyHospitableHornet.gif
   :width: 728 px

Requirements
------------

-  Wagtail >= 2.7
-  Django >= 2.0


Installing
----------

Install using pypi

.. code:: bash

    pip install wagtailannotatedimage

Using
-----

Extend the BaseAnnotationForm to define what data should be stored with annotations.
AnnotationsField stores the annotations data as a Dict with id for the annotation being the key.

.. code:: python

    from django.db import models
    from wagtail.wagtailcore.models import Page
    from wagtailannotatedimage.edit_handlers import AnnotatedImagePanel
    from wagtailannotatedimage.fields import AnnotationsField
    from wagtailannotatedimage.forms import BaseAnnotationForm

    class AnnotationForm(BaseAnnotationForm):


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

.. code:: html+Django
    {% image page.image('width-500') %}

    {% for annotation in page.annotations %}
    <div
     class='annotation'
     style="left: {{ annotation.x * 100 }}%; top: {{ annotation.y * 100 }}%;"
    >
        {{ annotations.fields.title }}
    </div>
    {% endfor %}
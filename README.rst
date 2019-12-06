Wagtail Annotated Image
=======================

Allows users to combine a Wagtail images with custom annotation data. Annotations are entered in the admin by
clicking points on an image, annotation data is then stored with relative x,y coordinates and optional extra form data.

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
AnnotationsField stores the annotations data as json, converting to a dict on retrieval.

.. code:: python

    from django import forms
    from django.db import models
    from wagtail.wagtailcore.models import Page
    from wagtailannotatedimage.edit_handlers import AnnotatedImagePanel
    from wagtailannotatedimage.fields import AnnotationsField
    from wagtailannotatedimage.forms import BaseAnnotationForm

    class AnnotationForm(BaseAnnotationForm):
        title = forms.CharField()
        about = forms.TextField()

    class TestPage(Page):
        image = models.ForeignKey('wagtailimages.Image', blank=True, null=True,
                                  on_delete=models.SET_NULL, related_name="+")
        annotations = AnnotationsField(blank=True)

        content_panels = Page.content_panels + [
            # First parameter - name of the image field
            # Second parameter - name of the annotation field
            # annotation_form - optional, the form used for annotations if you need to store data for each point
            AnnotatedImagePanel(
                'image', 'annotations',
                annotation_form=AnnotationForm(), heading='Annotated Image'
            )
        ]

.. code:: html+Django
    
    <div class='image-container'>
        {% image page.image('width-500') %}

        {% for annotation in page.annotations %}
        <div
            class='annotation'
            style="left: {{ annotation.x * 100 }}%; top: {{ annotation.y * 100 }}%;"
        >
            <h3>{{ annotation.fields.title }}</h3>
            <p>{{ annotation.fields.about }}</p>
        </div>
        {% endfor %}
    </div>

.. code:: css

    .image-container {
        position: relative;
    }

    .image-container > img {
        width: 100%;
        height: auto;
    }

    .annotation {
        position: absolute;
    }
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from wagtail.images.models import Filter
from wagtail.images import get_image_model

Image = get_image_model()


def get_full_image_url(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if image:
        filter = Filter(spec='original')
        orig_rendition = image.get_rendition(filter)
        return HttpResponse(orig_rendition.img_tag())
    else:
        return HttpResponse('')

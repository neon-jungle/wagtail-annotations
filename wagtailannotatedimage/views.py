from django.http import HttpResponse
from wagtail.wagtailimages.models import Filter, Image


def get_full_image_url(request, image_id):
    image = Image.objects.get(id=image_id)
    if image:
        filter, _ = Filter.objects.get_or_create(spec='original')
        orig_rendition = image.get_rendition(filter)
        return HttpResponse(orig_rendition.img_tag())
    else:
        return HttpResponse('')

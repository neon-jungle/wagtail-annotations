from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html, format_html_join
from wagtail.wagtailcore import hooks

from .views import get_full_image_url


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^full_image/(\d+)/$', get_full_image_url),
    ]


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('annotated-image/annotated-image.css')
    )


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'annotated-image/annotated-image-handler.js',
        'annotated-image/jquery.annotate.js',
    ]
    return format_html_join('\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

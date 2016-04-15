from __future__ import unicode_literals

from django import template
from django.core.urlresolvers import reverse

from django.contrib.contenttypes.models import ContentType

from ..authorization import load_can_delete, load_can_edit
from ..forms import CommentForm
from ..models import Comment

register = template.Library()


@register.simple_tag
@register.filter
def comment_count(object):
    """
    Usage:
        {% comment_count obj %}
    or
        {% comment_count obj as var %}
    """
    return Comment.objects.filter(
        object_id=object.pk,
        content_type=ContentType.objects.get_for_model(object)
    ).count()


@register.simple_tag
def comments(object):
    """
    Usage:
        {% comments obj as var %}
    """
    return Comment.objects.filter(
        object_id=object.pk,
        content_type=ContentType.objects.get_for_model(object)
    )


@register.simple_tag(takes_context=True)
def comment_form(context, object):
    """
    Usage:
        {% comment_form obj as comment_form %}
    Will read the `user` var out of the contex to know if the form should be
    form an auth'd user or not.
    """
    user = context.get("user")
    form_class = context.get("form", CommentForm)
    form = form_class(obj=object, user=user)
    return form


@register.simple_tag
def comment_target(object):
    """
    Usage:
        {% comment_target obj [as varname] %}
    """
    return reverse("post_comment", kwargs={
        "content_type_id": ContentType.objects.get_for_model(object).pk,
        "object_id": object.pk
    })

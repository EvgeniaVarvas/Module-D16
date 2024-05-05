from django import template
from django.utils.safestring import mark_safe
import bleach



register = template.Library()

def filter_video_and_images(value):
    allowed_tags = ['a', 'b', 'em', 'strong', 'p'] 
    cleaned_value = bleach.clean(value, tags=allowed_tags, strip=True)
    return mark_safe(cleaned_value)

register.filter('filter_video_and_images', filter_video_and_images)




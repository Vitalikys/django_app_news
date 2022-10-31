#https://docs.djangoproject.com/en/4.0/howto/custom-template-tags/
# in file.html  need to import this file
from django import template
from django.db.models import Count, F

from blog.models import Category

register = template.Library()

@register.simple_tag(name='get_list_categories')
def get_categories():
    # categories = Category.objects.annotate(cnt= Count('news')).filter(cnt__gt=0)
    # якшо потрібно врахцваьти що не опубліковакні
    categories = Category.objects.annotate(cnt= Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    return categories

@register.inclusion_tag('blog/list_categor_inclusion_tag.html')
def show_categories(arg = 'same menu ver.inclusion_Tag:'):
    categories = Category.objects.all()
    return {'categories': categories, 'arg':arg}
 # зразу робить рендер в шаблон,   'arg' для прикладу. не обовязково }
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import News, Category, Reviews


# user: admin       passw: admin
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    # fields to show in admin add form:
    fields = (
        'title', 'category', 'content', 'photo', 'get_photo', \
        'photo_url', 'is_published', 'created_at', 'updated_at', 'views')
    readonly_fields = ('get_photo', 'created_at', 'updated_at', 'views')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src ="{obj.photo.url}" width="35">')

    save_on_top = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)  # leave , it's tuple


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    fields = ('email', 'name', 'text', 'parent', 'news', 'created_review_at')
    list_display = ('name', 'text', 'news')
    readonly_fields = ('news', 'created_review_at')
    search_fields = ('text',)


admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'новинa Title admin'
admin.site.site_header = 'Керування сайтом новин Site headere'
# Register your models here.

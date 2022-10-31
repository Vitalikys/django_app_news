from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
from django.db import models
from django.urls import reverse
# all info from:
# https://www.youtube.com/watch?v=moR7m2-tkxs&list=PLmC7X4gkQWCeyIdLxHZdts-3tkcrxP4-o&index=8&ab_channel=Progercourse
# Create your models here.


class News(models.Model, HitCountMixin):
    title= models.CharField(max_length=150 ) #verb_name  is for admin.site
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата створення')
    updated_at = models.DateField(auto_now=True)
    # photo add to different folders /Y +  /m
    photo = models.ImageField(upload_to='photos/%Y/%m/', blank=True)
    photo_url = models.CharField(max_length=150, blank=True, default='https://picsum.photos/id/1011/350/235')
    is_published  =models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    views = models.IntegerField(default=0)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def get_absolute_url(self):
        return reverse('article_detail_url', kwargs={'pk':self.pk})

    #  добавляємо щоб в консолі shell можна бачити при визові New.objects.all()
    def __str__(self):
        return self.title

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    # добавляємо щоб в AдмінЦі було нормально підписано, так як ми задамо
    class Meta:
        verbose_name= 'Новина'
        verbose_name_plural = 'Новини'
        ordering = ['-created_at'] # sort by

# створюємо і додаємо в class: News^
class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Категорія')
    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title
    class Meta:         # for admin.menu
        verbose_name= 'Категорія'
        verbose_name_plural = 'Категорії'


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Ім'я", max_length=30)
    text = models.TextField("Повідомлення", max_length=200)
    parent = models.ForeignKey('self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True)
    news = models.ForeignKey(News, verbose_name="стаття", on_delete=models.CASCADE)
    created_review_at = models.DateTimeField(verbose_name='дата відгука', auto_now_add=True)

    def __str__(self):
        return'Comment by: "{}" on: \"{}" '.format(self.name, self.news)

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ('created_review_at',)


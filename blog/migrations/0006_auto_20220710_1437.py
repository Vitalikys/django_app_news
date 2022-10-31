# Generated by Django 3.2.13 on 2022-07-10 11:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_reviews'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviews',
            options={'ordering': ('created_review_at',), 'verbose_name': 'Відгук', 'verbose_name_plural': 'Відгуки'},
        ),
        migrations.AddField(
            model_name='reviews',
            name='created_review_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

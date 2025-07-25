# Generated by Django 5.2.1 on 2025-05-29 15:18

import apps.blog.models
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField()),
                ('thumbnail', models.ImageField(upload_to=apps.blog.models.category_thumbnail_directory)),
                ('slug', models.CharField(max_length=128)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blog.category')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=256)),
                ('content', models.TextField()),
                ('thumbnail', models.ImageField(upload_to=apps.blog.models.blog_thumbnail_directory)),
                ('keywords', models.CharField(max_length=128)),
                ('slug', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.category')),
            ],
            options={
                'ordering': ('status', '-created_at'),
            },
        ),
        migrations.CreateModel(
            name='Heading',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('level', models.IntegerField(choices=[(1, 'H1'), (2, 'H2'), (3, 'H3'), (4, 'H4'), (5, 'H5'), (6, 'H6')])),
                ('order', models.PositiveIntegerField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='headings', to='blog.post')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]

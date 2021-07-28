# Generated by Django 3.2.5 on 2021-07-28 18:59
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sku', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=False, verbose_name='is_active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('updated_at',),
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.IntegerField(choices=[(1, 'Product Created'), (2, 'Product Updated'), (3, 'Product Deleted')], default=1)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AddConstraint(
            model_name='subscriber',
            constraint=models.UniqueConstraint(fields=('event', 'url'), name='unique_url_for_an_event'),
        ),
    ]

# Generated by Django 2.1.5 on 2020-01-22 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0006_auto_20200121_0445'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='followed_by',
            field=models.ManyToManyField(blank=True, default=[], related_name='followed_items',
                                         to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='store',
            name='items',
        ),
        migrations.AddField(
            model_name='item',
            name='store',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='has_items',
                                    to='shops.Store'),
        ),
        migrations.AlterField(
            model_name='store',
            name='followed_by',
            field=models.ManyToManyField(blank=True, default=[], null=True, related_name='followed_stores',
                                         to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set(),
        )
    ]

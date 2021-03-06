# Generated by Django 2.0 on 2020-01-19 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_auto_20200118_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentOutstanding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_store_payment', to='shops.Store')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_payment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'payment_outstanding',
            },
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='paid',
        ),
        migrations.AddField(
            model_name='purchase',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]

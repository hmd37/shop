# Generated by Django 5.1.4 on 2024-12-07 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price_usd', models.PositiveIntegerField(default=0)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('is_vip', models.BooleanField(default=False)),
            ],
        ),
    ]

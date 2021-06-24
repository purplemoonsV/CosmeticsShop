# Generated by Django 3.2.3 on 2021-06-17 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_alter_carts_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('Fav_id', models.AutoField(primary_key=True, serialize=False)),
                ('pro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.member')),
            ],
        ),
    ]

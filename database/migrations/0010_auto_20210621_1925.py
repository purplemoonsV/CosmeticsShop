# Generated by Django 3.2.3 on 2021-06-21 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_auto_20210619_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='favourite',
            field=models.ManyToManyField(related_name='user_favourite', to='database.Member'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default='2021-06-21', null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='pay_date',
            field=models.DateTimeField(default='2021-06-21', null=True),
        ),
        migrations.DeleteModel(
            name='Favourite',
        ),
    ]

# Generated by Django 4.2.13 on 2024-05-16 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructionapp', '0003_designerbooking_contractorbooking_architectbooking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserName', models.CharField(max_length=200)),
                ('User_ID', models.IntegerField()),
                ('Account_Number', models.CharField(max_length=200)),
                ('Cvv', models.IntegerField()),
                ('ExpiryDate', models.CharField(max_length=200)),
            ],
        ),
    ]

# Generated by Django 4.2.10 on 2024-03-30 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_movie', '0006_alter_seat_seat_row'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_no',
            field=models.AutoField(max_length=10, primary_key=True, serialize=False),
        ),
    ]

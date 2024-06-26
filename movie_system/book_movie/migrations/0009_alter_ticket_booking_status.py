# Generated by Django 4.2.10 on 2024-03-30 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_movie', '0008_alter_ticket_ticket_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='booking_status',
            field=models.CharField(choices=[('BOOKED', 'BOOKED'), ('CANCELED', 'CANCELED')], default='BOOKED', max_length=24, null=True),
        ),
    ]

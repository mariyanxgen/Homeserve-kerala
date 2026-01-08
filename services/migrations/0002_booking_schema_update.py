# Generated manually to align Booking model with current schema
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        # Rename customer_notes -> notes
        migrations.RenameField(
            model_name='booking',
            old_name='customer_notes',
            new_name='notes',
        ),
        # Add fields for customer details
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(
                related_name='bookings',
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.SET_NULL,
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name='booking',
            name='customer_name',
            field=models.CharField(max_length=200, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='customer_email',
            field=models.EmailField(max_length=254, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='customer_phone',
            field=models.CharField(max_length=15, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='customer_address',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='is_emergency',
            field=models.BooleanField(default=False),
        ),
        # Remove legacy location and payment fields
        migrations.RemoveField(
            model_name='booking',
            name='address',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='city',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='pincode',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='estimated_duration',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='payment_status',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='customer',
        ),
    ]

# Generated by Django 4.2.2 on 2023-07-02 16:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0005_payment_orderplace'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPlaced',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('ordered_data', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Kabul Edildi', 'Kabul Edildi'), ('Kargo Hazırlandı', 'Kargo Hazırlandı'), ('Kargo Gönderildi', 'Kargo Gönderildi'), ('Teslim Edildi', 'Teslim Edildi'), ('İptal', 'İptal'), ('Kargo Bekliyor', 'Kargo bekliyor')], default='Kargo bekliyor', max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.kullanici')),
                ('payment', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.urun')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='OrderPlace',
        ),
    ]

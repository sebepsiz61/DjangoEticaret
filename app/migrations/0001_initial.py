# Generated by Django 4.2.2 on 2023-06-20 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Urun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('satis_fiyati', models.FloatField()),
                ('indirimli_fiyat', models.FloatField()),
                ('urun_aciklama', models.TextField()),
                ('detay', models.TextField(default='')),
                ('ekle', models.TextField(default='')),
                ('kategori', models.CharField(choices=[('PC', 'Bilgisayar'), ('TB', 'Tablet'), ('LT', 'Laptop'), ('WD', 'Web Tasarım'), ('SW', 'Yazılım'), ('DT', 'Veri Kurtarma'), ('MH', 'Muhasebe'), ('FA', 'Format')], max_length=2)),
                ('urun_foto', models.ImageField(upload_to='urunler')),
            ],
        ),
    ]

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
ANA_KATEGORi= (
    ('PC' ,'Bilgisayar'),
    ('SG' ,'Siber Güvenlik'),
    ('LT' ,'Laptop'),
    ('WT' ,'Web Tasarım'),
    ('SW' ,'Yazılım'),
    ('DT' ,'Veri Kurtarma'),
    ('MH' ,'Muhasebe'),
    ('FA' ,'Format'),
)

ILLER_IL= (
    ('01' , 'ADANA'),
    ('02' , 'ADIYAMAN'),
    ('03' , 'AFYONKARAHİSAR'),
    ('04' , 'AĞRI'),
    ('05' , 'AMASYA'),
    ('06' , 'ANKARA'),
    ('07' , 'ANTALYA'),
    ('08' , 'ARTVİN'),
    ('09' , 'AYDIN'),
    ('10' , 'BALIKESİR'),
    ('11' , 'BİLECİK'),
    ('12' , 'BİNGÖL'),
    ('13' , 'BİTLİS'),
    ('14' , 'BOLU'),
    ('15' , 'BURDUR'),
    ('16' , 'BURSA'),
    ('17' , 'ÇANAKKALE'),
    ('18' , 'ÇANKIRI'),
    ('19' , 'ÇORUM'),
    ('20' , 'DENİZLİ'),
    ('21' , 'DİYARBAKIR'),
    ('22' , 'EDİRNE'),
    ('23' , 'ELAZIĞ'),
    ('24' , 'ERZİNCAN'),
    ('25' , 'ERZURUM'),
    ('26' , 'ESKİŞEHİR'),
    ('27' , 'GAZİANTEP'),
    ('28' , 'GİRESUN'),
    ('29' , 'GÜMÜŞHANE'),
    ('30' , 'HAKKARİ'),
    ('31' , 'HATAY'),
    ('32' , 'ISPARTA'),
    ('33' , 'MERSİN'),
    ('34' , 'İSTANBUL'),
    ('35' , 'İZMİR'),
    ('36' , 'KARS'),
    ('37' , 'KASTAMONU'),
    ('38' , 'KAYSERİ'),
    ('39' , 'KIRKLARELİ'),
    ('40' , 'KIRŞEHİR'),
    ('41' , 'KOCAELİ'),
    ('42' , 'KONYA'),
    ('43' , 'KÜTAHYA'),
    ('44' , 'MALATYA'),
    ('45' , 'MANİSA'),
    ('46' , 'KAHRAMANMARAŞ'),
    ('47' , 'MARDİN'),
    ('48' , 'MUĞLA'),
    ('49' , 'MUŞ'),
    ('50' , 'NEVŞEHİR'),
    ('51' , 'NİĞDE'),
    ('52' , 'ORDU'),
    ('53' , 'RİZE'),
    ('54' , 'SAKARYA'),
    ('55' , 'SAMSUN'),
    ('56' , 'SİİRT'),
    ('57' , 'SİNOP'),
    ('58' , 'SİVAS'),
    ('59' , 'TEKİRDAĞ'),
    ('60' , 'TOKAT'),
    ('61' , 'TRABZON'),
    ('62' , 'TUNCELİ'),
    ('63' , 'ŞANLIURFA'),
    ('64' , 'UŞAK'),
    ('65' , 'VAN'),
    ('66' , 'YOZGAT'),
    ('67' , 'ZONGULDAK'),
    ('68' , 'AKSARAY'),
    ('69' , 'BAYBURT'),
    ('70' , 'KARAMAN'),
    ('71' , 'KIRIKKALE'),
    ('72' , 'BATMAN'),
    ('73' , 'ŞIRNAK'),
    ('74' , 'BARTIN'),
    ('75' , 'ARDAHAN'),
    ('76' , 'IĞDIR'),
    ('77' , 'YALOVA'),
    ('78' , 'KARABÜK'),
    ('79' , 'KİLİS'),
    ('80' , 'OSMANİYE'),
    ('81' , 'DÜZCE'),

)

class Urun(models.Model):
    title = models.CharField(max_length=100)
    satis_fiyati = models.FloatField()
    indirimli_fiyat = models.FloatField()
    urun_aciklama = models.TextField()
    detay = models.TextField(default='')
    ekle = models.TextField(default='')
    kategori = models.CharField(choices=ANA_KATEGORi, max_length=2)
    urun_foto = models.ImageField(upload_to='urunler')

    def __str__(self):
        return self.title
    

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=ILLER_IL,max_length=100)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    urun = models.ForeignKey(Urun,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.urun.indirimli_fiyat
    

STATUS_CHOICES = (
    ('Kabul Edildi','Kabul Edildi'),
    ('Kargo Hazırlandı','Kargo Hazırlandı'),
    ('Kargo Gönderildi','Kargo Gönderildi'),
    ('Teslim Edildi','Teslim Edildi'),
    ('İptal','İptal'),
    ('Kargo Bekliyor','Kargo bekliyor'),
)

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    urun = models.ForeignKey(Urun,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Kargo bekliyor')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    
    
    @property
    def total_cost(self):
        return self.quantity * self.urun.indirimli_fiyat

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    urun = models.ForeignKey(Urun,on_delete=models.CASCADE)
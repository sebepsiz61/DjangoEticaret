from django.contrib import admin
from . models import Customer,Payment,Urun,Cart, OrderPlaced,Wishlist
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group


# Register your models here.
@admin.register(Urun)
class UrunAdmin(admin.ModelAdmin):
    list_display = ['id','title','indirimli_fiyat','kategori','urun_foto']


@admin.register(Customer)
class KulaniciModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city', 'state','zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','urun','quantity']
    def urun(self,obj):
        link= reverse("admin:app_product_change", args=[obj.urun.pk])
        return format_html('<a href={}">{}</a>',link, obj.urun.title)

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlaceModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customers','uruns','quantity','ordered_data','status','payments']
    def customers(self,obj):
        link= reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href={}">{}</a>',link, obj.customer.name)
    
    def uruns(self,obj):
        link= reverse("admin:app_urun_change", args=[obj.urun.pk])
        return format_html('<a href={}">{}</a>',link, obj.urun.title)
    
    def payments(self,obj):
        link= reverse("admin:app_payment_change", args=[obj.payment.pk])
        return format_html('<a href={}">{}</a>',link, obj.payment.razorpay_payment_id)
    
    


@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','uruns']
    def uruns(self,obj):
        link= reverse("admin:app_urun_change", args=[obj.urun.pk])
        return format_html('<a href={}">{}</a>',link, obj.urun.title)

admin.site.unregister(Group)
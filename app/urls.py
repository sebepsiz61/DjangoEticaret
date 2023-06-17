from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_view
from . forms import GirisForm, SifreSifirlamaForm, SifreDegisim,SifreSifirlamaSetForm

urlpatterns = [
    path('', views.Anasayfa, name='index'),
    path('hakkimizda', views.Hakkimizda, name='hakkimizda'),
    path('iletisim', views.Iletisim, name='iletisim'),
    path('kategori/<slug:val>', views.Kategori.as_view(), name='kategori'),
    path('kategori-baslik/<val>', views.KategoriBaslik.as_view(), name='kategori-baslik'),
    path('urun-detay/<int:pk>', views.UrunDetay.as_view(), name='urun-detay'),
    path('profilim/', views.Profilim.as_view(), name='profilim'),
    path('adres/', views.Adres, name='adres'),
    path('adresguncelle/<int:pk>', views.AdresGuncelle.as_view(), name='adresguncelle'),
    
    #CART -Sepet Ekleme
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),

    path('search/', views.search, name='search'),
    path('wishlist/', views.show_wishlist, name='showwishlist'),

    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('pluswishlist/',views.plus_wishlist),
    path('minuswishlist/',views.minus_wishlist), 


    # kayıt  bölümü
    path('kayitol/', views.KullaniciKayit.as_view(), name='kayit-ol'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=GirisForm), name='login'),
    path('sifredegis/', auth_view.PasswordChangeView.as_view(template_name='app/sifredegis.html',form_class=SifreDegisim, success_url='/sifredegistamam'), name='sifredegis'),
    path('sifredegistamam/', auth_view.PasswordChangeDoneView.as_view (template_name='app/sifredegistamam.html'), name='sifredegistamam'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),  
    
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=SifreSifirlamaForm), name='password_reset'),
    path('password-reset-done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),   
    path('password-reset-confirm/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=SifreSifirlamaSetForm), name='password_reset_confirm'),   
    path("password-reset-complete/", auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete')

]
urlpatterns = urlpatterns+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header ="Ecval Bilişim Yönetim"
admin.site.site_title ="Ecval Bilişim"
admin.site.site_index_title ="Hoş Geldiniz Ecval Bilişim "
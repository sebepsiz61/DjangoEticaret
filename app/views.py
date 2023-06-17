from django.db.models import Count
from django.http import JsonResponse
import razorpay #ödeme sistemi paytr gibi....pip install ?? olarak python aktif eedilmesi gerekmektedir.
from django.shortcuts import render, redirect
from django.views import View
from app.models import Customer
from . models import OrderPlaced, Urun,Cart,Payment,Wishlist
from . forms import KullaniciKayıtForm,ProfilimForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

def Anasayfa(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/anasayfa.html',locals())


def Hakkimizda(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/hakkimizda.html',locals())


def Iletisim(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/iletisim.html',locals())


class Kategori(View):
    def get(self,request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        urun = Urun.objects.filter(kategori=val)
        baslik =  Urun.objects.filter(kategori=val).values('title')#.annotate(total=Count('title'))
        return render(request, 'app/kategori.html',locals())


class KategoriBaslik(View):
    def get(self,request,val):
        urun = Urun.objects.filter(title=val)
        baslik =  Urun.objects.filter(kategori=urun[0].kategori).values('title')
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/kategori.html',locals())

@method_decorator(login_required,name='dispatch') 
class UrunDetay(View):
        def get(self,request,pk):
            urun = Urun.objects.get(pk=pk)
            wishlist = Wishlist.objects.filter(Q(urun=urun)& Q(user=request.user))
            totalitem = 0
            wishitem = 0
            if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
                wishitem = len(Wishlist.objects.filter(user=request.user))
            return render(request,"app/urundetay.html",locals())


class KullaniciKayit(View):
    def get(self,request):
        form = KullaniciKayıtForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/kayitol.html', locals())
    def post(self,request):
        form = KullaniciKayıtForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tebrikler ! başarıyla Kayıt Oldunuz')
        else:
            messages.warning(request, 'Yanlış Veri Girişi !!!')
        return render(request, 'app/kayitol.html',locals())

@method_decorator(login_required,name='dispatch')
class Profilim(View):
    def get(self,request):
        form = ProfilimForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profilim.html',locals())
    def post(self,request):
        form = ProfilimForm(request.POST)
        if form.is_valid():
                user = request.user
                name = form.cleaned_data['name']
                locality = form.cleaned_data['locality']
                city = form.cleaned_data['city']
                mobile = form.cleaned_data['mobile']
                state = form.cleaned_data['state']
                zipcode = form.cleaned_data['zipcode']

                reg = Customer(user=user,
                                name=name,
                                locality=locality,
                                mobile=mobile,
                                city=city,
                                state=state,
                                zipcode=zipcode)
                reg.save()
                messages.success(request,'Tebrikler ! Başarıyla Kayıt Oldunuz...')
        else:
                messages.warning(request, 'Yanlış Veri ')
        return render(request, 'app/profilim.html',locals())


@login_required
def Adres(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/adres.html',locals())

@method_decorator(login_required,name='dispatch')
class AdresGuncelle(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = ProfilimForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/adresguncelle.html',locals())
    def post(self,request,pk):
        form = ProfilimForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,'Tebrikler ! Başarıyla Güncellendi...')
        else:
            messages.warning(request, 'Başarısız Güncelleme')
        return redirect('adres')

@login_required
def add_to_cart(request):
    user=request.user
    urun_id=request.GET.get('prod_id')
    urun = Urun.objects.get(id=urun_id)
    Cart(user=user,urun=urun).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount= 0
    for p in cart:
        value = p.quantity * p.urun.indirimli_fiyat
        amount = amount + value
    totalamount = amount + 1
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html', locals())

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    urun = Wishlist.objects.filter(user=user)
    return render(request, "app/wishlist.html",locals())

@method_decorator(login_required,name='dispatch') 
class checkout(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.urun.indirimli_fiyat
            famount = famount + value
        totalamount = famount + 1
        odemeamount = int(totalamount * 100 )
        client = razorpay.Client(auth=(settings.ODEME_KEY_ID, settings.ODEME_KEY_SECRET))
        data = {"amount": odemeamount, "currency": "INR", "receipt": "order_rcptid_12"}
        odeme_response = client.order.create(data=data)
        #print(odeme_response)
        #{'id':'order_M96QdPI8B0Xdp4','entity':'order','amount': 39500,'amount_paid':0,'amount_due':39500,'currency':'INR','receipt':'order_rcptid_12','offer_id':None,'status':'created','attempts':0,'notes':[], 'created_at':1688338007}
        order_id = odeme_response['id']
        order_status = odeme_response['status']
        if order_status == 'created':
            payment = Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request, 'app/checkout.html', locals())

@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    #print("payment_done : oid = ",order_id," pid = ",payment_id," cid = " ,cust_id)
    user = request.user
    #return redirect("orders")
    customer = Customer.objects.get(id=cust_id)
    #To update payment status and payment id
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    #To save order detalies
    cart = Cart.objects.filter(user=user)
    for c in Cart:
        OrderPlaced(user=user,customer=customer,urun=c.urun,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("orders")

@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(urun=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.urun.indirimli_fiyat
            amount = amount + value
            totalamount = amount + 100  
        #print(prod_id)        
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(urun=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.urun.indirimli_fiyat
            amount = amount + value
            totalamount = amount + 100  
        #print(prod_id)        
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    


    
def remove_cart(request):
    global totalamount
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(urun=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.urun.indirimli_fiyat
            amount = amount + value
        totalamount = amount + 100                 
        data={
            'amount':amount,
            'totalamount':totalamount           
        }
        return JsonResponse(data)

def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        urun = Urun.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,urun=urun).save()
        data={
            'message':'Beğeni Listesine Eklendi',
        }
        return JsonResponse(data)
    

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        urun = Urun.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,urun=urun).delete()
        data={
            'message':'Beğeni Listesinden Kaldırıldı.',
        }
        return JsonResponse(data)

@login_required  
def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    urun = Urun.objects.filter(Q(title__icontains=query))
    return render(request, "app/search.html",locals())
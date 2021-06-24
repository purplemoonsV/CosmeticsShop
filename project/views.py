from django.shortcuts import render,redirect
from django.utils.tree import Node
from .forms import *
from database.models import *
from django.db.models import Q,Sum,Count
from django.core.paginator import Paginator
from django.contrib import messages
from PIL import Image
import os
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf #created in step 4

#---------------------REPORT
def report_order(request):
    data = {
            'order':Order.objects.all()
        }
    pdf = render_to_pdf('pdf/invoice.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def report_orderdetail(request,id):
    o = Order.objects.get(order_id=id)
    data = {
            'order':OrderDetail.objects.filter(order_id=id),
            'total':o.Total
        }
    pdf = render_to_pdf('pdf/report_orderDetail.html', data)
    return HttpResponse(pdf, content_type='application/pdf')



def index(request):
    return render(request,'index.html')

def isLogin(request):
    chk = True
    if '_admin' not in request.session:
        chk = False
    return chk

def isLoginU(request):
    chk = True
    if 'id' not in request.session:
        chk = False
    return chk

def login(request):
 #ถ้ามีเซสชันให้เข้าระบบจัดการข้อมูล 
    # if 'id' in request.session:
    #     return redirect('mem_management')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            try:
                data = Member.objects.get(email=email,password=password)
                if data is not None:
                    messages.success(request,"เข้าสู่ระบบสำเร็จ")
                    request.session['id']= data.mem_id
                    request.session['firstname']=data.firstname
                    return redirect('Index')
            except Member.DoesNotExist:
                messages.error(request,"ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้องกรุณาลองใหม่")
                return redirect('Login')
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})

def loginAdmin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            data = Admin.objects.get(user=email,password=password)
            
            if data is not None:
                request.session['_admin']= data.id
                messages.success(request,"เข้าสู่ระบบสำเร็จ")
                return redirect('Dashborad')
    else:
        form = LoginForm()
    return render(request,'LoginAdmin.html',{'form':form})

    # if 'id' in request.session:
    #     return redirect('mem_management')
    # if request.method == "POST":
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         email = form.cleaned_data["email"]
    #         password = form.cleaned_data["password"]
    #         data = Member.objects.get(Q(email=email)&Q(password=password))
    #         if data:
    #             request.session['id']=data.id
    #             request.session['firstname']=data.firstname
    #             return redirect('mem_management')
    # else:
    #     form = LoginForm()

    # vars = {'form':form}
    # return render(request,'member_login.html',vars)

def logout(request):
    del request.session["id"]
    del request.session["firstname"]
    messages.success(request,"ออกจากระบบสำเร็จ")
    return redirect("/")

def logoutA(request):
    del request.session["_admin"]
    messages.success(request,"ออกจากระบบสำเร็จ")
    return redirect("/")

def MemberManagement(request):
    # ถ้ายังไม่ login ให้ไปเพจเข้าระบบ
    if not isLogin(request):
        return redirect(('/'))
    data = Member.objects.all()
    memlabel = MemberForm()
    return render(request,'member_management.html',{'Members':data,'memlabel':memlabel})


def register(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            m = Member.objects.get(email=email)
            Carts.objects.create(cart_id=m.mem_id,user_id_id = m.mem_id)
            messages.success(request,"สมัครสมาชิกสำเร็จ")
            return redirect('/login')
    else:
        form = MemberForm()
    return render(request,"register.html",{'form':form})


def MemberUpdate(request, id):
    if request.method=="POST":
        data = Member.objects.get(mem_id=id)
        form = MemberForm(instance=data, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"แก้ไขข้อมูลสำเร็จ")
        return redirect('Index')
    else:
        data = Member.objects.get(mem_id=id)
        form = MemberForm(initial=data.__dict__)
    vars = {'form':form}
    return render(request,'member_form.html',vars)

def MemberDelete(request, id):
    data = Member.objects.get(mem_id=id).delete()
    if data is not None:
        messages.success(request,"ลบข้อมูลสำเร็จ")
    return redirect('mem_management')

#----------------------------------------------


def ProductManagement(request):
    #ถ้ายังไม่ login ให้ไปเพจเข้าระบบ
    if not isLogin(request):
        return redirect(('/'))
    data = Product.objects.all()
    prolabel = ProductForm()
    return render(request, 'product_management.html', {'data':data,'prolabel':prolabel})

def pro_detaill(request,id):
    if request.method == 'POST':
        addCart(request)
        return redirect('Carts')
    data = Product.objects.get(pro_id=id)
    review = Reviews.objects.filter(pro_id=id)
    c_review = review.count()
    return render(request,'product_detail.html',{'products':data,'review':review,'c_review':c_review})

    
def ProductCreate(request):
    if not isLogin(request):
        return redirect(('/'))
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            pd = form.save()
            messages.success(request,"เพิ่มข้อมูลสำเร็จ")
            pid = pd.pro_id 
        for f in files:
            pd_img = ProductImage(product_id = pid, image_file=f)
            pd_img.file_format = f.content_type.split('/')[1]
            pd_img.file_name = f.name
            pd_img.content_type = f.content_type
            pd_img.save()
        return redirect('/admin/product/')
    else:
        form = ProductForm()

    return render(request, 'product_form.html', {'form':form})


def ProductUpdate(request, id):
    if not isLogin(request):
        return redirect(('/'))
    if request.method == 'POST':
        row = Product.objects.get(pro_id=id)
        form = ProductForm(instance=row, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save() 
            files = request.FILES.getlist('files')
            messages.success(request,"แก้ไขข้อมูลสำเร็จ")
            if len(files) > 0:
                product_image = ProductImage.objects.filter(product_id = id)
                for p in product_image:
                    url = p.image_file.url
                    deletefileproduct(url)
                product_image.delete()
            for f in files:
                pd_img = ProductImage(product_id=id, image_file=f)
                pd_img.file_format = f.content_type.split('/')[1]
                pd_img.file_name = f.name
                pd_img.content_type = f.content_type
                pd_img.save()
        return redirect('/admin/product/')
    else:
        row = Product.objects.get(pro_id=id)
        form = ProductForm(instance=row)
        form.fields['pro_id'].widget.attrs['readonly'] = True
    return render(request, 'product_form.html', {'form':form})

def ProductDelete(request, id):
    product = Product.objects.get(pro_id=id)
    product.delete()

    product_image = ProductImage.objects.filter(product_id = id)
    if product is not None:
        messages.success(request,"ลบข้อมูลสำเร็จ")
    for p in product_image:
        url = p.image_file.url
        deletefileproduct(url)
        product_image.delete()
    return redirect('/admin/product/')

def deletefileproduct(imagepath):
    img = imagepath[1:]
    if os.path.exists(img):
        print("deleted succesfully")
        os.remove(img)
    else:
        print("The file does not exist")

#----------------------------------------------
def shop(request):    
    try:
        data = Product.objects.all()
        id =request.session["id"]
        m = Member.objects.get(mem_id = id)
        return render(request,'shopping.html',{'product':data,'m':m})
    except:
        data = Product.objects.all()
        return render(request,'shopping.html',{'product':data})
        

def ShopCate(request,id):
    data = Product.objects.filter(cate_id_id = id)
    return render(request,'shopping.html',{'product':data})

def dashborad(request):
    if not isLogin(request):
        return redirect(('/'))
    countm = Member.objects.count()
    countp = Product.objects.count()
    counto = Order.objects.count()
    countno = Order.objects.filter(statusOrder= 0).count()
    context = {'countm':countm,'countp':countp,'counto':counto,'countno':countno}
    return render(request,'dashborad.html',context)
#----------------------------------------------
def Categorys(request):
    if not isLogin(request):
        return redirect(('/'))
    data = Category.objects.all()
    catelabel = CategoryForm()
    return render(request, 'category_management.html', {'data':data,'catelabel':catelabel})

def CategoryUpdate(request, id):
    if not isLogin(request):
        return redirect(('/'))
    if request.method=="POST":
        data = Category.objects.get(cate_id=id)
        form = CategoryForm(instance=data, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"แก้ไขข้อมูลสำเร็จ")
        return redirect('cate_management')
    else:
        data = Category.objects.get(cate_id=id)
        form = CategoryForm(initial=data.__dict__)
    vars = {'form':form}
    return render(request,'category_form.html',vars)

def CategorysDelete(request, id):
    data = Category.objects.get(cate_id=id).delete()
    if data is not None:
        messages.success(request,"ลบข้อมูลสำเร็จ")
    return redirect('cate_management')

def CategorysCreate(request):
    if not isLogin(request):
        return redirect(('/'))
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"เพิ่มข้อมูลสำเร็จ")
            return redirect('cate_management')
    else:
        form = CategoryForm()
    return render(request,"category_form.html",{'form':form})

#----------------------------------------------
def Sizes(request):
    if not isLogin(request):
        return redirect(('/'))
    data = Size.objects.all()
    label = SizeForm()
    return render(request, 'size_management.html', {'data':data,'label':label})

def SizeUpdate(request, id):
    if not isLogin(request):
        return redirect(('/'))
    if request.method=="POST":
        data = Size.objects.get(sizes_id=id)
        form = SizeForm(instance=data, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"แก้ไขข้อมูลสำเร็จ")
        return redirect('size_management')
    else:
        data = Size.objects.get(sizes_id=id)
        form = SizeForm(initial=data.__dict__)
    vars = {'form':form}
    return render(request,'size_form.html',vars)

def SizeDelete(request, id):
    data = Size.objects.get(sizes_id=id).delete()
    if data is not None:
        messages.success(request,"ลบข้อมูลสำเร็จ")
    return redirect('size_management')

def SizeCreate(request):
    if not isLogin(request):
        return redirect(('/'))
    if request.method == "POST":
        form = SizeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"เพิ่มข้อมูลสำเร็จ")
            return redirect('size_management')
    else:
        form = SizeForm()
    return render(request,"size_form.html",{'form':form})

#----------------------------------------------
def ref_total(request):
    id = request.session["id"]
    sumx = CartItem.objects.filter(cart_id_id=id).aggregate(sum_price=Sum('Totals'))
    Carts.objects.filter(cart_id=id).update(Total=sumx['sum_price'])


def Cart(request): 
    if  'Checkout' in request.POST:#ถ้าเป็นเช็คเอ้าท์ให้ไปฟังชันก์ชอ.
        Checkout(request)
        return redirect('payment_create')
    elif 'Update' in request.POST: #เหมือนชอ.
        updatecarts(request)
        return redirect('Carts')

    id = request.session["id"]
    cart = Carts.objects.get(user_id=id)
    cart_item = CartItem.objects.filter(cart_id=id)

    return render(request,"carts.html",{'cart':cart,'item':cart_item})

def addCart(request):
    quantitys = request.POST["qty"]
    idp = request.POST["idp"]
    id = request.session["id"]
    pro = Product.objects.get(pro_id=idp)
    q=int(quantitys)
    CartItem.objects.create(cart_id_id=id,pro_id_id=idp,quantity=q,Totals=pro.price*q)
    sumx = CartItem.objects.filter(cart_id_id=id).aggregate(sum_price=Sum('Totals'))
    Carts.objects.filter(cart_id=id).update(Total=sumx['sum_price'])
    return redirect('Carts')

def DeleteItem(request,id):
    data = CartItem.objects.get(Item_id=id).delete()
    ref_total(request)
    messages.success(request,"ลบรายการเรียบร้อยแล้ว")
    return redirect('Carts')

def updatecarts(request):
    id = request.session["id"] #เก็บเซสซั่นไอดีไว้ที่ไอดี
    data = CartItem.objects.filter(cart_id_id=id) #หาตะกร้าที่มันตรงกับไอดี
    q=[]
    if data is not None: # สร้างลิสเก็บไว้ในq ถ้าตาด้าไม่ใช่ค่าว่างก็จะให้วนลูป
        for key, quantitys in request.POST.items(): #ให้วนลูปที่รีเควส.โพส คือการที่จะดึงคีกับแวลูมา
            if key[0] == 'q': #ถ้าคีย์จะให้มันเป็นตัวอักษรแรกที่อยู่ในคีย์มา แล้วเช็คว่าถ้าเท่ากับqให้ำการแอดวล.เข้าไปใส่ในคิวลิส
                q.append(quantitys)
        i = 0
        total = 0
        for item in data:
            sum = int(q[i])*item.pro_id.price
            item.quantity=int(q[i])
            item.Totals=sum
            total += sum
            i+=1
            item.save()
    data.filter(quantity=0).delete()
    Carts.objects.filter(cart_id=id).update(Total=total)
    messages.success(request,"อัพเดตรายการเรียบร้อยแล้ว")
        
    

# def AddUpdateItem(request,id):
#     data = CartItem.objects.get(Item_id=id)
#     data.quantity += 1
#     data.Totals = data.pro_id.price * data.quantity
#     data.save()
#     sumx = CartItem.objects.filter(cart_id_id=data.cart_id_id).aggregate(sum_price=Sum('Totals'))
#     Carts.objects.filter(cart_id=data.cart_id_id).update(Total=sumx['sum_price'])
#     return redirect('Carts')

# def RemoveUpdateItem(request,id):
#     data = CartItem.objects.get(Item_id=id)
#     data.quantity -= 1
#     data.Totals = data.pro_id.price * data.quantity
#     data.save()
#     sumx = CartItem.objects.filter(cart_id_id=data.cart_id_id).aggregate(sum_price=Sum('Totals'))
#     Carts.objects.filter(cart_id=data.cart_id_id).update(Total=sumx['sum_price'])
#     return redirect('Carts')

def Checkout(request):
    if request.method == 'POST':
        id = request.session["id"]
        cart = Carts.objects.get(cart_id=id)
        item = CartItem.objects.filter(cart_id_id=id)
        order = Order.objects.create(mem_id=cart.user_id,Total=cart.Total,statusOrder=False)
        request.session["odid"] = order.order_id
        for items in item:
            OrderDetail.objects.create(order_id_id=order.order_id,pro_id_id = items.pro_id_id,quantity=items.quantity,Totals=items.Totals)
        cart.Total = 0
        cart.save()
        item.delete()
    return redirect('payment_create')

#================Orders====================
def Orders(request):
    if not isLogin(request):
        return redirect(('/'))
    # if request.method == 'POST':
    #     report_order(request)
    data = Order.objects.all()
    label = OrderForm()
    memlabel = MemberForm()
    vars= {'data':data,'label':label,'memlabel':memlabel}
    return render(request, 'order_management.html', vars)


def OrderDelete(request, id):
    if not isLogin(request):
        return redirect(('/'))
    data = Order.objects.get(order_id=id).delete()
    if data is not None:
        messages.success(request,"ลบข้อมูลสำเร็จ")
    return redirect('order_management')


def OrderDetails(request, id):
    if not isLogin(request):
        return redirect(('/'))
    data = OrderDetail.objects.filter(order_id_id=id)
    label = OrderDetailForm()
    prolabel = ProductForm()
    vars = {'data':data,'label':label,'prolabel':prolabel}
    return render(request, 'orderdetail.html',vars )

#================Payment====================
def PaymentCreate(request):
    id = request.session["odid"]
    mem_data = Order.objects.get(order_id = id) 
    if request.method == 'POST':
        form = Payment.objects.create(order_id_id = id)
        
        # PaymentForm(request.POST, request.FILES)
        # if form.is_valid():
        files = request.FILES.getlist('files')
            # pay = form.save()
        payid = form.pay_id
        messages.success(request,"ชำระเงินเสร็จสิ้น")
        for f in files:
            pm_img = PaymentImage(payment_id = payid, image_file=f)
            pm_img.file_format = f.content_type.split('/')[1]
            pm_img.file_name = f.name
            pm_img.content_type = f.content_type
            pm_img.save()
        return redirect('/')
    else:
        form = PaymentForm()
    return render(request, 'payment_formx.html', {'form':form,'member':mem_data})


def Payments(request):
    if not isLogin(request):
        return redirect(('/'))
    data = Payment.objects.all()
    label = PaymentForm()
    vars= {'data':data,'label':label}
    return render(request, 'payment_management.html', vars)
    
def Confirm(request,id):
    if not isLogin(request):
        return redirect(('/'))
    data = Order.objects.get(order_id=id)
    data.statusOrder = 1
    data.save()
    messages.success(request,"ยืนยันคำสั่งซื้อเรียบร้อยแล้ว")
    return redirect('payment_management')

# Reviews
def Review(request,id):
    if request.method == 'POST':
        con = request.POST['content']
        mem = request.session["id"]
        re = Reviews.objects.create(content = con,pro_id = id,user_id=mem)
        if re is not None:
            messages.success(request,"ขอบคุณสำหรับการรีวิวสินค้า")
    return redirect('pro_detaill',id=id)
    # return render(request, 'product_detail.html')

# def AddFavourite(request,id):
#     idu = request.session["id"]
#     Favourite.objects.create(pro_id = id,user_id=idu)
#     messages.success(request,"เพิ่มสิ่งที่ถูกใจแล้ว")
#     return redirect('Shop')

def FavouriteList(request):
    idu = request.session["id"]
    m = Member.objects.get(mem_id = idu)
    list = Product.objects.filter(favourite=m)
    if list is None:
        messages.success(request,"ยังไม่มีสิ่งที่ท่านถูกใจ")
    return render(request,'FavouriteList.html',{'list':list})

def add_product(request,pk):
     product = get_object_or_404(Product,pro_id=pk)
     id =request.session["id"]
     m = Member.objects.get(mem_id = id)
     if m not in product.favourite.all():
         product.favourite.add(m)
     return redirect('Shop')

def remove_product(request,pk):
     product = get_object_or_404(Product,pro_id=pk)
     id =request.session["id"]
     m = Member.objects.get(mem_id = id)
     if m in product.favourite.all():
         product.favourite.remove(m)
     return redirect('Shop')

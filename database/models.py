from django.db import models
from django import forms
from django.db.models.fields.related import ForeignKey
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import widgets
from django.forms.fields import CharField
from django.utils import timezone, dateformat


#ผู้ดูแลระบบ
class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    user= models.CharField(unique=True,max_length=150)
    password= models.CharField(max_length=20)

class AdminForm(forms.ModelForm):
    class Meta:
        model= Admin
        fields= '__all__'
        labels= {
            'email':'อีเมล์',
            'password':'รหัสผ่าน',
        }
        widgets={
            'password': forms.PasswordInput(render_value=True)
        }



#สมาชิก
class Member(models.Model):
    mem_id = models.AutoField(primary_key=True)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    email=models.CharField(unique=True,max_length=150)
    password=models.CharField(max_length=10)
    tell = models.CharField(max_length=10,null=True,blank=True)
    address = models.CharField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return str(self.firstname)

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        labels= {
            'mem_id': 'รหัสสมาชิก',
            'firstname': 'ชื่อ',
            'lastname':'นามสกุล',
            'email':'อีเมล์',
            'password':'รหัสผ่าน',
            'tell':'เบอร์โทร',
            'address':'ที่อยู่',
    }
        widgets={
            'password': forms.PasswordInput(render_value=True)
    }



#ประเภทสินค้า
class Category(models.Model):
    cate_id = models.AutoField(primary_key=True)
    cate_type = models.CharField(max_length=20)

    def __str__(self):
        return str(self.cate_type)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        labels = {
            'cate_id':'รหัสประเภท',
            'cate_type':'ชื่อประเภท',
        }



#Size
class Size(models.Model):
    sizes_id = models.AutoField(primary_key=True)  
    sizes_pro = models.CharField(max_length=20)

    def __str__(self):
        return str(self.sizes_pro)


class SizeForm(forms.ModelForm):
     class Meta:
        model = Size
        fields = '__all__'
        labels = {
            'sizes_id':'รหัสขนาด',
            'sizes_pro':'ขนาด',
        }



#สินค้า
class Product(models.Model):
    pro_id = models.CharField(primary_key=True,max_length=5)
    pro_name = models.CharField(max_length=500)
    cate_id = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)
    brand = models.CharField(max_length=100)
    price = models.IntegerField()
    stock = models.IntegerField()
    description = models.TextField()
    sizes = models.ForeignKey(Size,null=True,on_delete=models.SET_NULL)
    ingredient = models.TextField()
    favourite = models.ManyToManyField(Member, related_name='user_favourite')

    def __str__(self):
        return str(self.pro_name)

class ProductForm(forms.ModelForm):
    files = forms.ImageField(required=False,
        widget=forms.ClearableFileInput(attrs={'multiple':True})
    )

    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'pro_id':'รหัสสินค้า',
            'pro_name':'ชื่อสินค้า',
            'category':'ประเภทสินค้า',
            'brand':'ผู้ผลิต',
            'price':'ราคา',
            'stock':'จำนวนสินค้า',
            'description':'รายละเอียด',
            'size':'ขนาด'
        }

class ProductImage(models.Model):
    product_id = models.CharField(max_length=5)
    image_file = models.ImageField(upload_to='product/')
    file_format = 'JPEG'
    file_name = 'unnamed.jpg'
    content_type = 'image/jpeg'

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if self.image_file:
            bio = BytesIO(self.image_file.read())
            img = Image.open(bio)
            max_size = (480, 640)
            img.thumbnail(max_size, Image.ANTIALIAS)
            buffer = BytesIO()
            img.save(buffer, self.file_format, quality=95)
            buffer.seek(0)
            self.image_file = InMemoryUploadedFile(
                buffer,
                'ImageField',
                self.file_name,
                self.content_type,
                buffer.__sizeof__,
                None
            )   
        super(ProductImage, self).save(*args, **kwargs)



#Carts
class Carts(models.Model):
    cart_id = models.CharField(primary_key=True,max_length=5)
    user_id = models.ForeignKey(Member,on_delete=models.CASCADE)
    Total = models.IntegerField(null=True,default=0)

class CartItem(models.Model):
    Item_id = models.AutoField(primary_key=True)
    cart_id = models.ForeignKey(Carts,on_delete=models.CASCADE)
    pro_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    Totals = models.IntegerField(default=0)


#ออเดอร์สินค้า
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateTimeField(default=dateformat.format(timezone.now(),'Y-m-d'),null=True)
    mem_id = models.ForeignKey(Member,on_delete=models.CASCADE)
    Total = models.PositiveIntegerField(default=0)
    statusOrder = models.BooleanField()

    def __str__(self):
        return str(self.order_id)
        
class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = '__all__'
        labels = {
            'order_id':'เลขที่สั่งซื้อ',
            'order_date':'เวลาสั่งซื้อ',
            'mem_id':'รหัสสมาชิก',
            'Total':'ราคารวม',
            'statusOrder':'สถานะการยืนยัน',
        }


#รายละเอียดออเดอร์สินค้า
class OrderDetail(models.Model):
    order_de_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    pro_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    Totals = models.IntegerField(default=0)

class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = '__all__'
        labels = {
            'order_de_id':'ลำดับการสั่งซื้อ',
            'order_id':'เลขที่สั่งซื้อ',
            'pro_id':'รหัสสินค้า',
            'quantity':'จำนวนสินค้า',
            'Totals':'รวมจำนวนสินค้า',
        }


#การชำระเงิน
class Payment(models.Model):
    pay_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    pay_date = models.DateTimeField(default=dateformat.format(timezone.now(),'Y-m-d'),null=True)

class PaymentForm(forms.ModelForm):
    files = forms.ImageField(required=False,
        widget=forms.ClearableFileInput(attrs={'multiple':True})
    )

    class Meta:
        model = Payment
        fields = '__all__'
        labels = {
            'pay_id':'รหัสชำระเงิน',
            'order_id':'เลขที่สั่งซื้อ',
            'pay_date':'วันที่ชำระเงิน',
        }

class PaymentImage(models.Model):
    payment_id = models.CharField(max_length=5)
    image_file = models.ImageField(upload_to='Payment/')
    file_format = 'JPEG'
    file_name = 'unnamed.jpg'
    content_type = 'image/jpeg'

    def save(self, *args, **kwargs):
        if self.image_file:
            bio = BytesIO(self.image_file.read())
            img = Image.open(bio)
            max_size = (480, 640)
            img.thumbnail(max_size, Image.ANTIALIAS)
            buffer = BytesIO()
            img.save(buffer, self.file_format, quality=95)
            buffer.seek(0)
            self.image_file = InMemoryUploadedFile(
                buffer,
                'ImageField',
                self.file_name,
                self.content_type,
                buffer.__sizeof__,
                None
            )   
        super(PaymentImage, self).save(*args, **kwargs)

#Reviews

class Reviews(models.Model):
    Re_id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=300)
    pro = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Member,on_delete=models.CASCADE)

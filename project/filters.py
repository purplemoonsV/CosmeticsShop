from django import template
from django.http import request
from database.models import *

register = template.Library()

@register.filter
def getimages(pid):
    return ProductImage.objects.filter(product_id=pid)
    
@register.filter
def getimagespay(pid):
    return PaymentImage.objects.filter(payment_id=pid)
    
@register.filter
def getimagesone(pid):
    data=ProductImage.objects.filter(product_id=pid)
    return data

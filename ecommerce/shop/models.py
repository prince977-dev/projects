from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=20)
    desc=models.TextField()
    image=models.ImageField(upload_to='media/image',blank=True,null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    p_name = models.CharField(max_length=20)
    p_desc = models.TextField()
    p_image = models.ImageField(upload_to='media/products', null=True, blank=True)
    p_stock = models.IntegerField()
    p_available = models.BooleanField(default=True)
    p_created = models.DateTimeField(auto_now_add=True)
    p_updated = models.DateTimeField(auto_now=True)
    p_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    p_price=models.IntegerField()

    def __str__(self):
        return self.p_name

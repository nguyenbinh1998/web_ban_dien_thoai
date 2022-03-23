from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('product_list_by_category', kwargs={'category_slug':self.slug})

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product/%Y/%m/%d", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    avaiable = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, db_index=True)

    class Meta:
        ordering = ['name',]
        index_together = (('id', 'slug'),)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_id':self.id, 'product_slug':self.slug})

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=10, decimal_places=2)

    def can_purchase(self, product):
        return self.budget >= product.price

    def __str__(self):
        return self.name
    def get_budget(self):
        num = self.budget
        return f"{num:,}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['date']

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None):
        if not phone_number:
            raise ValueError('The Phone Number is required')
        if not name:
            raise ValueError('The Name is required')
        user = self.model(phone_number=phone_number, name=name)
        user.set_password(password)
        user.username = self.generate_username(name)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password=None):
        user = self.create_user(phone_number, name, password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def generate_username(self, name):
        username = name.lower().replace(' ', '_')
        if self.model.objects.filter(username=username).exists():
            count = self.model.objects.filter(username__startswith=username).count()
            username = f'{username}_{count+1}'
        return username

class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Add this line

    objects = MyUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.phone_number




from django.db import models
from django.conf import settings

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    num_of_people = models.IntegerField()
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} at {self.time}"
    



# myapp/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=100, blank=True, null=True)
    special = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    

class PopularMenuItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='popular_menu_images/', blank=True, null=True)

    def __str__(self):
        return self.name



# models.py

from django.db import models
from django.conf import settings

class CustomerOrder(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('ready', 'Ready'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delivery_preference = models.CharField(max_length=10)
    delivery_time = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    apt_number = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    card_number = models.CharField(max_length=16)
    card_expiry = models.CharField(max_length=5)
    card_cvc = models.CharField(max_length=3)
    order_date = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sales_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"



class CustomerOrderItem(models.Model):
    order = models.ForeignKey(CustomerOrder, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.name} for Order {self.order.id}"




from django.db import models
from django.conf import settings

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.rating}'


